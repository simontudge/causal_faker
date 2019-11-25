# causal_faker

Fake data generator in which the user specifies a causal graph and fake data is generated. The user specifies a weighted DAG from which fake data can be generated.

## Assumptions

Random variables are drawn from a normal distribution.

All dependencies are linear (can relax this assumption later)

## Example Use

See the notebook: ./`notebooks/examples.ipynb`

## Causal Inference Notebooks

In addition to the main module of fake data generation I also create a number of notebooks that look into the key ideas in causal inference. They are here because they often make use of the fake data generation module.
