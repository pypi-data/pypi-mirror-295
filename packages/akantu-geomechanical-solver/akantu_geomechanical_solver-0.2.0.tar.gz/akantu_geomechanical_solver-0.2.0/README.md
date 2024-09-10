# Akantu Geomechanica Solver

_Python package containing a geomechanical simulator based on the open-source FEM library [Akantu](https://gitlab.com/akantu/akantu)_

[![PyPI version](https://badge.fury.io/py/akantu-geomechanical-solver.svg)](https://badge.fury.io/py/akantu-geomechanical-solver)
[![Project Status](https://img.shields.io/badge/status-under%20development-yellow)](https://gitlab.com/hsolleder/akantu-geomechanical-solver)
![GitLab License](https://img.shields.io/gitlab/license/hsolleder%2Fakantu-geomechanical-solver)

See the package documentation on [GitLab Pages](https://akantu-geomechanical-solver-hsolleder-7af331464042e47dbd537897e.gitlab.io/)

# Installation

## Serial

``` bash
pip install akantu-geomechanical-solver
```

## Parallel

### Pull the Docker image

To use the Docker image including a parallel version of the geomechanical solver, follow these steps:

1. Make sure you have Docker installed on your system.
2. Pull the Docker image from the registry using the following command:

```bash
docker pull registry.gitlab.com/hsolleder/akantu-geomechanical-solver/parallel-gms-images:main
```

3. Once the image is pulled, you can run a container using the image with the following command:

```bash
docker run -it registry.gitlab.com/hsolleder/akantu-geomechanical-solver/parallel-gms-images:main
```

This will start a container and give you an interactive shell inside it.

4. You can now use the Docker image for your desired purposes.

### Build from source

Start by cloning the repository, for instance using

```bash
git clone git@gitlab.com:hsolleder/akantu-geomechanical-solver.git
```

Then, use the `installation.sh` script to setup the parallel version of akantu hydromechanical coupling branch on your machine.

You can then install the parallel version version of the geomechanical solver

``` bash
pip install .[parallel]
```
