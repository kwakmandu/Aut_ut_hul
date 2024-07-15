from block.block_4byte import Block4Byte
from ssd.storage_device_interface import StorageDeviceInterface
import pandas as pd
import os


class VirtualSSD(StorageDeviceInterface):
    def __init__(self):
        self.nand_path = "ssd/nand.csv"
        self.result_path = "ssd/result.csv"

        if not os.path.exists(self.nand_path):
            self.nand_df = pd.DataFrame(columns=["Data"], data=["0x00000000"] * 100)
            self.nand_df.to_csv(self.nand_path)

    def write(self, addr: int, data: str) -> None:
        self.nand_df = pd.read_csv(self.nand_path)
        self.nand_df.iloc[addr] = data
        self.nand_df.to_csv(self.nand_path)

    def read(self, address: int) -> None:
        pass


ssd = VirtualSSD()
