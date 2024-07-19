from abc import ABC, abstractmethod
from ssd.strategy import DequeStrategy, InterfaceStrategy, HeapStrategy


class InterfaceStrategyFactory(ABC):
    @abstractmethod
    def select_strategy(self, strategy_name: str) -> InterfaceStrategy:
        pass


class StrategyFactory(InterfaceStrategyFactory):
    def select_strategy(self, strategy_name: str) -> InterfaceStrategy:
        if strategy_name.upper() == "DEQUE":
            return DequeStrategy()
        elif strategy_name.upper() == "HEAP":
            return HeapStrategy()

        return HeapStrategy()
