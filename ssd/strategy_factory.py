from abc import ABC, abstractmethod
from ssd.strategy import DequeStrategy, InterfaceStrategy


class InterfaceStrategyFactory(ABC):
    @abstractmethod
    def select_strategy(self, strategy_name: str) -> InterfaceStrategy:
        pass


class StrategyFactory(InterfaceStrategyFactory):
    def select_strategy(self, strategy_name: str) -> InterfaceStrategy:
        if strategy_name == "Deque":
            return DequeStrategy()
        return DequeStrategy()
