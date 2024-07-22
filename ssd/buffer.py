import os
from typing import List

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
        strategy="Heap",
        csv_path=os.path.join(".", "buffer.csv"),
    ) -> None:
        self.__cmd_list_limit_size = cmd_list_limit_size
        self.__strategy = StrategyFactory().select_strategy(strategy)
        self.__csv_path = csv_path
        self.__csv_header = None
        self.__cmd_list: list[BufferCmd] = self._load_csvfile_and_set_cmd_list()

    def add_cmd(self, cmd_type: str, address: int, value: str) -> None:
        if self._is_invalid():
            raise Exception("Invalid error occur")

        self.__cmd_list = self.__strategy.update(
            self.__cmd_list, BufferCmd(cmd_type, address, value)
        )
        self._save_buffer_csv()

    def read_addressvalue_in_cmdlist(self, address: int) -> str | None:
        rst_value = self.__strategy.read(self.__cmd_list, address)  # value or None
        return rst_value

    def _select_strategy(self, strategy: str) -> InterfaceStrategy:
        return StrategyFactory().select_strategy(strategy)

    def _is_invalid(self) -> bool:
        return len(self.__cmd_list) >= self.__cmd_list_limit_size

    def _load_csvfile_and_set_cmd_list(self) -> list[BufferCmd]:
        if not os.path.exists(self.__csv_path):
            init_df = pd.DataFrame(columns=["command", "address", "value"])
            init_df.to_csv(self.__csv_path, index=False)
        df = pd.read_csv(self.__csv_path)
        self.__csv_header = df.columns.tolist()  # 헤더 저장
        cmd_list = [
            BufferCmd(cmd_type, address, str(value))
            for cmd_type, address, value in df.values.tolist()
        ]
        return cmd_list

    def get_cmd_list_limit_size(self) -> int:
        return self.__cmd_list_limit_size

    def get_size(self) -> int:
        return len(self.__cmd_list)

    def get_cmd_list(self) -> list[BufferCmd]:
        return self.__cmd_list

    def _save_buffer_csv(self) -> None:
        cmd_list_converted_to_list = []
        for cmd in self.__cmd_list:
            cmd_list_converted_to_list.append([cmd.type, cmd.address, cmd.value])
        df = pd.DataFrame(cmd_list_converted_to_list, columns=self.__csv_header)
        df.to_csv(self.__csv_path, index=False, header=True)

    def flush(self) -> None:
        self.__cmd_list = []
        self._save_buffer_csv()
