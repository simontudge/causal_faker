import numpy as np
from scipy.sparse import dok_matrix


class CycleError(ValueError):
    pass


class CausalFaker:
    """
    Main class that represents a linear causal graph, as well as generating
    fake data based on that graph.
    
    User inputs a DAG, where each node represents a variable.
    
    Nodes without parents are drawn from a normal distibution
    
    The values of all other nodes are given by deterministic equations
    based on the weights of the graph.
    
    Raises:
    -------
    CycleError if the input graph contains cycles (Not a Dag)
    
    """
    
    def __init__(self, weights):
        """
        Inputs
        ------
    
        weights: dict (2-tuple): set(int)
        Specify each edge of the graph and its weight.
        See example use below
        
        Example Use
        -----------

        ```PYTHON
        from random import random
        weights = {
            (0, 1): random(),
            (1, 4): random(),
            (1, 5): random(),
            (2, 3): random(),
            (3, 1): random(),
            (3, 4): random(),
            (4, 5): random()
        }

        cf = CausalFaker(6, weights)
        ```
        """

        self.weights = weights
        
        # Set the number of nodes in total 
        self.nodes = set()
        for e in self.weights.keys():
            self.nodes.add(e[0])
            self.nodes.add(e[1])

        self.nodes = list(self.nodes)
        
        self.nodes.sort()
        self.n = max(self.nodes) + 1
        
        self._set_adj_dicts()

        self._set_node_levels()

    def _set_adj_dicts(self):
        # From this representation we can make the adjacency list
        # as well as the inverse (links children to parents.)
        self.adj = {i: set() for i in self.nodes}
        self.adj_inv = {i: set() for i in self.nodes}

        for a, b in self.weights.keys():
            self.adj[a].add(b)
            self.adj_inv[b].add(a)

    def _set_node_levels(self):

        found_nodes = set()
        node_levels = []

        i = 0
        while len(found_nodes) < self.n:
            next_set = {k for k, v in self.adj_inv.items() if len(v - found_nodes) == 0}
            node_levels.append(next_set - found_nodes)
            found_nodes.update(next_set)
            i += 1
            if i > self.n:
                print('Maximum level exceeded, which means your graph has cycles')
                raise CycleError

        self.node_levels = node_levels

    def _random(self):
        return np.random.normal(0, 1)

    def get_values(self):
        """
        Returns a dictionary of variables, representing one set of random variables
        """

        variable_values = {}

        # Do first of all the first ones, as these are special cases.
        for edge in self.node_levels[0]:
            variable_values[edge] = self._random()

        # Now loop through the rest, excluding the first level
        for edges in self.node_levels[1:]:
            for edge in edges:
                parents = self.adj_inv[edge]
                partial_values = [self.weights[(parent, edge)]*variable_values[parent]
                                  for parent in parents]

                variable_values[edge] = sum(partial_values)

        return variable_values

    def get_n(self, n):
        """
        Return n examples of random data.
        """
        
        return [self.get_values() for _ in range(n)]
    
    def get_df(self, n):
        """
        Get n examples, and return as a pandas dataframe, the columns
        of which are the different variables, the rows are the different
        trials.
        """
        try:
            import pandas as pd
        except ImportError:
            print('Install pandas')
            raise ImportError

        return pd.DataFrame(self.get_n(n))

    @property
    def depth(self):
        return len(self.node_levels)
    
    @property
    def adjaceny_matrix(self):
        """
        Returns the adjecency matrix.
        """
        
        try:
            return self._adj_matrix
        except AttributeError:
            am = np.zeros((self.n, self.n))
            for edge, weight in self.weights.items():
                am[edge[0], edge[1]] = weight
            self._adj_matrix = am
            return self._adj_matrix
        
    @property
    def scipy_sparse(self):
        
        try:
            return self._sparse
        except AttributeError:
            
            S = dok_matrix((self.n, self.n), dtype=np.float32)
            for edge, weight in self.weights.items():
                S[edge[0], edge[1]] = weight
                
            self._sparse = S
            return S
        
    @property
    def networkx(self):
        
        try:
            from networkx import DiGraph
        except ImportError:
            print('Install networkX')
            raise ImportError
        
        try:
            return self._nx
        except AttributeError:
            nx = DiGraph(self.adjaceny_matrix)
            self._nx = nx
            return nx
        
    def draw(self):

        try:
            import networkx as nx
        except ImportError:
            print('Install networkX')
            raise ImportError
    
        return nx.draw_networkx(self.networkx)

    def pretty_print_equation(self):
        """
        Give a list of equations representing the graphs.
        """

        for n in self.nodes:
            # Get a list of tuples, first is the v
            parents = self.adj_inv[n]
            if len(parents) == 0:
                right_side = 'N(0, 1)'
            else:
                right_side = ' + '.join(['{:.3f}*x_{}'.format(self.weights[i, n], i)
                                         for i in parents])
            
            right_side.replace('+ -', '-')
            print('x_{} = {}'.format(n, right_side))



