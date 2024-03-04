from pydantic import BaseModel
from allokate.backends.base import Backend
from allokate.types import AllokateRequest, AllokatableDeployment
from typing import Protocol, runtime_checkable


@runtime_checkable
class Pod(Protocol):

    def restart(self):
        pass



class Allokater(BaseModel):
    backend: Backend


    def allocate(self, rekuest: AllokateRequest) -> Pod:	
        return self.backend.allocate(rekuest.allokatable_deployments[0], command=rekuest.command)

    
    class Config:
        arbitrary_types_allowed = True