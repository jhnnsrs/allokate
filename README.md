# allokate

A simple selector based allocation library for Python, that aims to allocate
pods on a variety of backends (e.g. Kubernetes, Docker, etc.) based on a
simple selector language.

## Installation

```bash
pip install allokate
```

## Usage

The following example demonstrates how to allocate a deployment with a minimum
of 1024MB of RAM, 1 CPU with a frequency of 2.5GHz and a CUDA compute
capability of 1 on a connected Docker backend.

```python
from allokate.allokater import Allokater
from allokate.backends.docker import DockerBackend
from allokate.types import AllokateRequest, AllokatableDeployment
from allokate.selectors import RAMSelector, CPUSelector, CudaSelector


allokater = Allokater(backend=DockerBackend())



request = AllokateRequest(
    allokatable_deployments=[
        AllokatableDeployment(
            selectors=[
                RAMSelector(type="ram", min=1024),
                CPUSelector(type="cpu", min=1, frequency=2.5),
                CudaSelector(type="cuda", compute_capability=1),
            ],
            flavour="vanilla",
            image="nvidia/cuda:12.3.2-base-ubuntu22.04",
        )
    ],
    command="nvidia-smi"
)

allokater.allocate(request)
```

The docker backend will then allocate a container on the host with the
requested resources and execute the command `nvidia-smi` inside the container.
If the resources are not available, the allocation will fail.

## Goals

Design goals for this library are:

- Simple and easy to use
- Support for a variety of backends
- Create more-userfriendly selectors for the user
- Support for a variety of resources (e.g. RAM, CPU, CUDA, etc.)
- Support for a variety of deployment types (e.g. Docker, Kubernetes, etc.)

## Development

This is a work in progress and contributions are welcome. Please see the
[CONTRIBUTING.md](CONTRIBUTING.md) file for more information.




