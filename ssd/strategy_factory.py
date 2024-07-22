from abc import ABC, abstractmethod
from ssd.strategy import DequeStrategy, InterfaceStrategy, HeapStrategy


class StrategyFactory:
    @staticmethod
    def select_strategy(strategy_name: str) -> InterfaceStrategy:
        match strategy_name.upper():
            case "DEQUE":
                return DequeStrategy()
            case "HEAP":
                return HeapStrategy()
            case _:
                return HeapStrategy()
