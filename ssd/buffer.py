import os
from collections import deque
from typing import List, Any

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
    def flush(self):
        pass


class Buffer(InterfaceBuffer):
    def __init__(
        self,
        cmdlist_limitsize=10,
        strategy="Deque",
        csv_path=os.path.join(".", "buffer.csv"),
    ):
        self.cmdlist_limitsize = cmdlist_limitsize
        self.strategy = self._select_strategy(strategy)
        self.csv_path = csv_path
        self.csv_header = None
        self.cmdlist = self._load_csvfile_and_set_cmdlist()

    def add_cmd(self, cmd_type: str, address: int, value: str) -> None:
        if self._is_invalid():
            raise Exception("Invalid error occur")

        new_cmd = (cmd_type, address, value)
        self.cmdlist = self.strategy.update(self.cmdlist, new_cmd)
        self._save_buffer_csv()

    def read_addressvalue_in_cmdlist(self, address: int) -> str:
        rst_value = self.strategy.read(self.cmdlist, address)  # value or None
        return rst_value

    def _select_strategy(self, strategy: str) -> DequeStrategy:
        if strategy == "Deque":
            return DequeStrategy()

    def _is_invalid(self) -> bool:
        if len(self.cmdlist) >= self.cmdlist_limitsize:
            return True

    def _load_csvfile_and_set_cmdlist(self) -> List[Any]:
        if not os.path.exists(self.csv_path):
            init_df = pd.DataFrame(columns=["command", "address", "value"])
            init_df.to_csv(self.csv_path, index=False)
        df = pd.read_csv(self.csv_path)
        self.csv_header = df.columns.tolist()  # 헤더 저장
        rows_as_lists = df.values.tolist()
        cmdlist = list(rows_as_lists)
        return cmdlist

    def get_cmdlist_limitsize(self) -> int:
        return self.cmdlist_limitsize

    def get_size(self) -> int:
        return len(self.cmdlist)

    def get_cmdlist(self) -> List[Any]:
        return self.cmdlist

    def _save_buffer_csv(self) -> None:
        df = pd.DataFrame(self.cmdlist, columns=self.csv_header)
        df.to_csv(self.csv_path, index=False, header=True)

    def flush(self) -> None:
        self.cmdlist = []
        self._save_buffer_csv()
