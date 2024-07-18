import os
from collections import deque
from dataclasses import dataclass
from typing import List, Any

import pandas as pd
from abc import ABC, abstractmethod

from ssd.buffer_cmd import BufferCmd
from ssd.strategy import DequeStrategy, InterfaceStrategy
from ssd.strategy_factory import StrategyFactory


class InterfaceBuffer(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def get_cmd_list(self) -> List[BufferCmd]:
        pass

    @abstractmethod
    def add_cmd(self, cmd_type: str, address: int, value: str) -> None:
        pass

    @abstractmethod
    def flush(self) -> None:
        pass


class Buffer(InterfaceBuffer):
    def __init__(
        self,
        cmd_list_limit_size=10,
        strategy="Deque",
        csv_path=os.path.join(".", "buffer.csv"),
    ) -> None:
        self.cmd_list_limit_size = cmd_list_limit_size
        self.strategy_factory = StrategyFactory()
        self.strategy = self.strategy_factory.select_strategy(strategy)
        self.csv_path = csv_path
        self.csv_header = None
        self.cmd_list: list[BufferCmd] = self._load_csvfile_and_set_cmd_list()

    def add_cmd(self, cmd_type: str, address: int, value: str) -> None:
        if self._is_invalid():
            raise Exception("Invalid error occur")

        self.cmd_list = self.strategy.update(
            self.cmd_list, BufferCmd(cmd_type, address, value)
        )
        self._save_buffer_csv()

    def read_addressvalue_in_cmdlist(self, address: int) -> str | None:
        rst_value = self.strategy.read(self.cmd_list, address)  # value or None
        return rst_value

    def _select_strategy(self, strategy: str) -> InterfaceStrategy:
        # TODO(gyu.byeon): 팩토리 패턴으로 변경
        if strategy == "Deque":
            return DequeStrategy()

    def _is_invalid(self) -> bool:
        return len(self.cmd_list) >= self.cmd_list_limit_size

    def _load_csvfile_and_set_cmd_list(self) -> list[BufferCmd]:
        if not os.path.exists(self.csv_path):
            init_df = pd.DataFrame(columns=["command", "address", "value"])
            init_df.to_csv(self.csv_path, index=False)
        df = pd.read_csv(self.csv_path)
        self.csv_header = df.columns.tolist()  # 헤더 저장
        cmd_list = [
            BufferCmd(cmd_type, address, value)
            for cmd_type, address, value in df.values.tolist()
        ]
        return cmd_list

    def get_cmd_list_limit_size(self) -> int:
        return self.cmd_list_limit_size

    def get_size(self) -> int:
        return len(self.cmd_list)

    def get_cmd_list(self) -> list[BufferCmd]:
        return self.cmd_list

    def _save_buffer_csv(self) -> None:
        cmdlist_converted_to_list = []
        for cmd in self.cmd_list:
            cmdlist_converted_to_list.append([cmd.type, cmd.address, cmd.value])
        df = pd.DataFrame(cmdlist_converted_to_list, columns=self.csv_header)
        df.to_csv(self.csv_path, index=False, header=True)

    def flush(self) -> None:
        self.cmd_list = []
        self._save_buffer_csv()
