from abc import ABC, abstractmethod


class AbstractCallback(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        raise NotImplementedError


class STDOUTCallback(AbstractCallback):

    def __call__(self, *args, **kwargs) -> None:
        print(args, kwargs)
