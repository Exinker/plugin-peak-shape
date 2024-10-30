from abc import ABC, abstractmethod


class AbstractCallback(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        raise NotImplementedError


class NullCallback(AbstractCallback):

    def __call__(self, *args, **kwargs) -> None:
        pass
