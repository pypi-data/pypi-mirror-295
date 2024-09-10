# README

<div align="center">
<img src="./assets/joplen_logo.svg" width="300">
</div>

---


This is the code for the [IEEE MLSP 2024](https://2024.ieeemlsp.org) workshop paper "Joint Optimization of Piecewise Linear Ensembles" [[arxiv](https://arxiv.org/abs/2405.00303)] [IEEE (coming soon)].
For now, please cite as

```bibtex
@misc{raymond2024,
    title={Joint Optimization of Piecewise Linear Ensembles},
    author={Matt Raymond and Angela Violi and Clayton Scott},
    year={2024},
    eprint={2405.00303},
    archivePrefix={arXiv},
    primaryClass={cs.LG},
    url={https://arxiv.org/abs/2405.00303},
}
```

The associated GitLab issue tracker is currently limited to internal use.
Please email [the current maintainer listed on PyPI](https://pypi.org/project/joplen/) with any questions or concerns, and they will open an issue on your behalf.

## Installation

### Installation via PyPI

```bash
pip install joplen
```

### Installation from source

*NOTE: `pip install -e .` will only work if you have setuptools v64 or higher and pip version 24 or higher.*

Clone the repository to your local machine, then run the following commands (which assume that you already have [Conda](https://docs.conda.io) installed):

```bash
conda create --prefix ./my_env python=3.10
conda activate ./my_env
conda config --set env_prompt '({name}) '

pip install -r requirements.txt
pip install -e .
```

JAX must be installed manually according to [this link](https://github.com/google/jax/discussions/16380) because the installation is hardware-dependent.
Please follow [these instructions](https://jax.readthedocs.io/en/latest/installation.html) to install JAX.

## Usage

Each module has example usage.
You can run them by executing the module as a script.
Note that single-task JOPLEn is much more modular than the multitask implementation.
This is for practical reasons, but there's no reason it couldn't be made more modular.

```bash
python -m JOPLEn.singletask # single-task joplen
python -m JOPLEn.multitask # multi-task joplen
python -m JOPLEn.competing # Friedman ensemble refitting
```

## Original implementation

To see the original implementation for the workshop submission, please see <https://gitlab.eecs.umich.edu/mattrmd-public/joplen-repositories/joplen-mlsp2024>.
