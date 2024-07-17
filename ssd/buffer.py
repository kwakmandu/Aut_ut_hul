import os
from collections import deque

import pandas as pd
from abc import ABC, abstractmethod

from ssd.strategy import DequeStrategy


class InterfaceBuffer(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_size(self):
        pass

    @abstractmethod
    def get_cmdlist(self):
        pass

    @abstractmethod
    def add_cmd(self):
        pass

    @abstractmethod
    def _load_csvfile_and_set_cmdlist(self):
        pass

    @abstractmethod
    def select_strategy(self, strategy):
        pass


class Buffer(InterfaceBuffer):
    def __init__(
        self, size=10, strategy="Deque", csv_path=os.path.join(".", "buffer.csv")
    ):
        self.size = size
        self.strategy = self.select_strategy(strategy)
        self.csv_path = csv_path
        self.cmdlist = self._load_csvfile_and_set_cmdlist()

    def _load_csvfile_and_set_cmdlist(self):
        df = pd.read_csv(self.csv_path)
        rows_as_lists = df.values.tolist()
        cmdlist = deque(rows_as_lists)
        return cmdlist

    def get_size(self):
        return len(self.cmdlist)

    def get_cmdlist(self):
        return self.cmdlist

    def add_cmd(self, command, address, value):
        new_command = (command, address, value)
        self.strategy.optimise(self.cmdlist, new_command)

    def select_strategy(self, strategy):
        if strategy == "Deque":
            return DequeStrategy()


bf = Buffer()
