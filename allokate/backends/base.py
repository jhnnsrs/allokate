from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod

@runtime_checkable
class Backend(Protocol):

    def allocate(self, *args, **kwargs):
        ...


class BaseBackend(ABC):

    @abstractmethod
    def allocate(self, *args, **kwargs):
        pass
