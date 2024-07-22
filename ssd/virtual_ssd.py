import sys
import warnings
from collections import deque
from typing import Optional

from logger.logger import Logger
from ssd.buffer import Buffer
from ssd.storage_device_interface import StorageDeviceInterface
import pandas as pd
import os

warnings.filterwarnings("ignore")
INIT_VALUE: str = "0x00000000"


class VirtualSSD(StorageDeviceInterface):
    def __init__(self, buffer: Buffer(strategy="Heap")) -> None:
        self.__logger = Logger()
        self.__buffer = buffer  # Heap, Deque
        self.__nand_path = "nand.csv"
        self.__result_path = "result.txt"

        if not os.path.exists(self.__nand_path):
            self.nand_df = pd.DataFrame(
                columns=["Data"], data=[("%s" % INIT_VALUE)] * 100
            )
            self.nand_df.to_csv(self.__nand_path)

        self.nand_df = pd.read_csv(self.__nand_path)

    def write(self, address: int, data: str) -> None:
        if self.__buffer.get_size() == 10:
            self.flush()
        self.__buffer.add_cmd("W", address, data)
        self.__logger.print("Data has been successfully written to the SSD.")

    def read(self, address: int) -> None:
        if os.path.exists(self.__result_path):
            os.remove(self.__result_path)

        read_data = None
        if self.__buffer.get_size() > 0:
            read_data = self.__buffer.read_addressvalue_in_cmdlist(address)

        if read_data is None:
            read_data = self.nand_df.loc[address, "Data"]
        elif read_data == "Erase":
            read_data = INIT_VALUE

        result_df = pd.DataFrame(data=[read_data], columns=["Data"])
        result_df = result_df.replace("\n", "")

        with open(self.__result_path, "w", encoding="utf-8") as file:
            file.write(str(result_df.loc[0, "Data"]))
        self.__logger.print("Data has been successfully read from the SSD.")

    def erase(self, address: int, size: str) -> None:
        if self.__buffer.get_size() == 10:
            self.flush()
        self.__buffer.add_cmd("E", address, size)
        self.__logger.print("SSD has been successfully erased.")

    def flush(self) -> None:
        deque_buffer = deque(self.__buffer.get_cmd_list())
        while deque_buffer:
            old_command = deque_buffer.popleft()
            address = old_command.address
            match old_command.type:
                case "W":
                    value = old_command.value
                    self.nand_df.loc[address, "Data"] = value
                    self.__logger.print(
                        f"Flushing... : write addr {address} = data {value}"
                    )
                case "E":
                    value = int(old_command.value)
                    self.nand_df.loc[address : address + int(value) - 1] = INIT_VALUE
                    self.__logger.print(
                        f"Flushing... : erase addr {address} to addr {address + value - 1}"
                    )
        self.__logger.print("SSD has been successfully flushed.")
        self.__buffer.flush()
        if os.path.exists(self.__nand_path):
            os.remove(self.__nand_path)
        self.nand_df["Data"].to_csv(self.__nand_path, index_label="index")

    def execute_command(
        self, cmd: str, address: Optional[str], value: Optional[str]
    ) -> None:
        if cmd == "W":
            if address is not None and value is not None:
                self.write(int(address), value)
        elif cmd == "R":
            if address is not None:
                self.read(int(address))
        elif cmd == "E":
            if address is not None and value is not None:
                self.erase(int(address), value)
        elif cmd == "F":
            self.flush()
        else:
            self.__logger.print("INVALID COMMAND")

    def set_buffer(self, buffer: Buffer) -> None:
        self.__buffer = buffer
