import os
import pandas as pd
from abc import ABC, abstractmethod


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


class Buffer(InterfaceBuffer):
    def __init__(
        self, size=10, strategy="Deque", csv_path=os.path.join(".", "buffer.csv")
    ):
        self.super().init()
        self.size = size
        self.strategy = strategy
        self.cmdlist = pd.read_csv("cmdlist.csv")

        pass

    def get_size(self):
        pass

    def get_cmdlist(self):
        pass

    def add_cmd(self):
        pass
