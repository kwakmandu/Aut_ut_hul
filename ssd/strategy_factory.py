from abc import ABC, abstractmethod
from ssd.strategy import DequeStrategy, InterfaceStrategy, HeapStrategy


class InterfaceStrategyFactory(ABC):
    @staticmethod
    @abstractmethod
    def select_strategy(strategy_name: str) -> InterfaceStrategy:
        pass


class StrategyFactory(InterfaceStrategyFactory):
    @staticmethod
    def select_strategy(strategy_name: str) -> InterfaceStrategy:
        if strategy_name.upper() == "DEQUE":
            return DequeStrategy()
        elif strategy_name.upper() == "HEAP":
            return HeapStrategy()

        return HeapStrategy()
