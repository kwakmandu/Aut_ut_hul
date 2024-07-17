import sys
from collections import deque
from typing import Optional

from logger.logger import Logger
from ssd.buffer import Buffer
from storage_device_interface import StorageDeviceInterface
from ssd.storage_device_interface import StorageDeviceInterface
import pandas as pd
import os

INIT_VALUE = "0x00000000"


class VirtualSSD(StorageDeviceInterface):
    def __init__(self) -> None:
        self.logger = Logger()
        self.nand_path = "nand.csv"
        self.result_path = "result.txt"

        if not os.path.exists(self.nand_path):
            self.nand_df = pd.DataFrame(
                columns=["Data"], data=[("%s" % INIT_VALUE)] * 100
            )
            self.nand_df.to_csv(self.nand_path)

        self.nand_df = pd.read_csv(self.nand_path)

    def write(self, address: int, data: str) -> None:
        if buffer.get_size() == 10:
            self.flush()
        else:
            buffer.add_cmd("W", address, data)

        self.logger.print("Data has been successfully written to the SSD.")

    def read(self, address: int) -> None:
        if os.path.exists(self.result_path):
            os.remove(self.result_path)

        read_data = None
        if buffer.get_size() > 0:
            read_data = buffer.read_addressvalue_in_cmdlist(address)
        if read_data is None:
            read_data = self.nand_df.loc[address, "Data"]

        result_df = pd.DataFrame(data=[read_data], columns=["Data"])
        result_df = result_df.replace("\n", "")

        with open(self.result_path, "w", encoding="utf-8") as file:
            file.write(str(result_df.loc[0, "Data"]))
        self.logger.print("Data has been successfully read from the SSD.")

    def erase(self, address: int, size: int) -> None:
        if buffer.get_size() == 10:
            self.flush()
        else:
            buffer.add_cmd("E", address, size)

        self.logger.print("SSD has been successfully erased.")

    def flush(self) -> None:
        while buffer.cmdlist:
            old_command = deque(buffer.cmdlist).popleft().strip().split()
            command1 = int(old_command[1])
            command2 = int(old_command[2])
            match old_command[0]:
                case "W":
                    self.nand_df.loc[command1, "Data"] = command2
                    self.logger.print(
                        f"Flushing... : write addr {command1} = data {command2}"
                    )
                case "E":
                    self.nand_df.loc[command1 : command1 + command2 - 1] = INIT_VALUE
                    self.logger.print(
                        f"Flushing... : erase addr {command1} to addr {command1 + command2 - 1}"
                    )
                    self.logger.print("SSD has been successfully flushed.")

        buffer.flush()
        if os.path.exists(self.nand_path):
            os.remove(self.nand_path)
        self.nand_df["Data"].to_csv(self.nand_path, index_label="index")
        self.logger.print("SSD has been successfully flushed.")


if __name__ == "__main__":
    ssd = VirtualSSD()
    buffer = Buffer()

    cmd: Optional[str]
    address: Optional[str]
    value: Optional[str]

    cmd, address, value = (sys.argv[1:4] + [None] * 3)[:3]

    if cmd == "W":
        if address is not None and value is not None:
            ssd.write(int(address), value)
    elif cmd == "R":
        if address is not None:
            ssd.read(int(address))
    elif cmd == "E":
        if address is not None and value is not None:
            ssd.erase(int(address), int(value))
    elif cmd == "F":
        ssd.flush()
