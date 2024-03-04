from allokate.backends.base import BaseBackend
import docker
from allokate.types import AllokatableDeployment
import subprocess
import json
import psutil
from allokate.selectors import RAMSelector, CPUSelector, CudaSelector
import xml.etree.ElementTree as ET
import xmltodict
from copy import copy
from rich import pretty
from rich import inspect
import semver
from packaging import version

pretty.install()



def get_nested_nullable(d, key):

    keys = key.split(".")

    for k in keys:
        try:
            d = d[k]
        except KeyError:
            return None

    return d


class DockerPod:

    def __init__(self, _client, container):
        self._client = _client
        self.container = container

    def restart(self):
        self._client.containers.restart(self.container.id)

class DockerBackend(BaseBackend):
    """ A local docker backend for allokate
    
    This backend uses the docker-py library to interact with the local docker daemon.
    and trys to allocate the deployment to the local machine

    """
    max_ram_for_containers = 1024
    nvidia_smi_image = "nvidia/cuda:12.3.2-base-ubuntu22.04"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = docker.from_env()


        memory = psutil.virtual_memory()

        self.total_ram = memory.total
        self.available_ram = memory.available

        self.total_cpu = psutil.cpu_count()
        self.available_cpu = psutil.cpu_count(logical=False)

        self.retrieve_gpu_info()


    def retrieve_gpu_info(self):

        self._client.images.pull(self.nvidia_smi_image)
        output = self._client.containers.run(self.nvidia_smi_image, "nvidia-smi -q -x",
            device_requests=[  # Request access to all GPUs
            docker.types.DeviceRequest(
                count=-1,
                capabilities=[['gpu']]
            )
        ],)
        root = xmltodict.parse(output)

        self.cuda_version = get_nested_nullable(root, "nvidia_smi_log.cuda_version")
        self.driver_version = get_nested_nullable(root, "nvidia_smi_log.driver_version")
        self.attached_gpus = get_nested_nullable(root, "nvidia_smi_log.attached_gpus")
        self.gpu_name = get_nested_nullable(root, "nvidia_smi_log.gpu.product_name")
        self.gpu_ram = get_nested_nullable(root, "nvidia_smi_log.gpu.fb_memory_usage.total")
        self.cuda_version = get_nested_nullable(root, "nvidia_smi_log.driver_version")

        print(self.gpu_name, self.gpu_ram)
    







    



    def allocate(self, deployment: AllokatableDeployment, command=None):


        device_requests = []
        docker_params = []

        # Check if the deployment is possible
        for selector in deployment.selectors:
            if isinstance(selector, RAMSelector):
                if selector.min > self.available_ram:
                    raise ValueError("Not enough RAM available")
                
            if isinstance(selector, CPUSelector):
                if selector.min > self.available_cpu:
                    raise ValueError("Not enough CPU available")
                
            if isinstance(selector, CudaSelector):
                if selector.cuda_version and version.parse(self.cuda_version) < version.parse(selector.cuda_version):
                    raise ValueError("CUDA version is too low")
                
                if selector.memory and selector.memory > self.gpu_ram:
                    raise ValueError("Not enough GPU RAM available")
                
                device_requests.append(docker.types.DeviceRequest(
                    count=-1,
                    capabilities=[['gpu']]
                ))


        print("Deployment is possible")


        # Allocate the deployment
        container = self._client.containers.run(deployment.image, command, detach=True, device_requests=device_requests, environment={"NVIDIA_VISIBLE_DEVICES": "all"})

        return DockerPod(self._client, container.id)


        return 






