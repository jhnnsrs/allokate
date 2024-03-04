from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from allokate.selectors import Selector





class AllokatableDeployment(BaseModel):
    """A deployment is a Release of a Build.
    It contains the build_id, the manifest, the builder, the definitions, the image and the deployed_at timestamp.



    """
    selectors: List[Selector] = Field(
        description="The selectors are used to place this image on the nodes",
        default_factory=list,
    )
    flavour: str = Field(
        description="The flavour that was used to build this deployment",
        default="vanilla",
    )
    image: str = Field(
        description="The docker image that was built for this deployment"
    )


class ComputeNode(BaseModel):

    def inspect(self):
        pass


class Deployment(BaseModel):

    def inspect_node(self) -> ComputeNode:
        pass





class AllokateRequest(BaseModel):
    allokatable_deployments: List[AllokatableDeployment] = Field(default_factory=list)
    command: str


