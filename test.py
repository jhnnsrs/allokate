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




pod = allokater.allocate(request)
