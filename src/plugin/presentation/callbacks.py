from abc import ABC, abstractmethod


class ProgressCallbackABC(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        raise NotImplementedError


class NullProgressCallback(ProgressCallbackABC):

    def __call__(self, *args, **kwargs) -> None:
        pass
