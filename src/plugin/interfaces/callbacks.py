from abc import ABC, abstractmethod


class AbstractProgressCallback(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        raise NotImplementedError


class NullProgressCallback(AbstractProgressCallback):

    def __call__(self, *args, **kwargs) -> None:
        pass
