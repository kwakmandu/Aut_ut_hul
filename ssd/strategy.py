from abc import ABC, abstractmethod


class InterfaceStrategy(ABC):
    @abstractmethod
    def update(self):
        pass


class DequeStrategy(InterfaceStrategy):
    def update(self):
        pass
