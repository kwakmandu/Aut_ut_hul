from abc import ABC, abstractmethod


class InterfaceStrategy(ABC):
    @abstractmethod
    def optimise(self):
        pass

class DequeStrategy(InterfaceStrategy):

    def optimise(self):
        pass