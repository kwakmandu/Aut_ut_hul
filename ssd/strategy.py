from abc import ABC, abstractmethod
from collections import deque


class InterfaceStrategy(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def read(self):
        pass


class DequeStrategy(InterfaceStrategy):
    def update(self, cmdlist, new_cmd):
        new_cmdlist = deque(cmdlist)

        return new_cmdlist

    def read(self, cmdlist, address):
        value = 0  # or None
        return value
