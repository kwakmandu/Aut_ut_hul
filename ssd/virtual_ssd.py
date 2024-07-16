import sys

from ssd.storage_device_interface import StorageDeviceInterface
import pandas as pd
import os

INIT_VALUE = "0x00000000"


class VirtualSSD(StorageDeviceInterface):
    def __init__(self) -> None:
        self.nand_path = "nand.csv"
        self.result_path = "result.csv"

        if not os.path.exists(self.nand_path):
            self.nand_df = pd.DataFrame(
                columns=["Data"], data=[("%s" % INIT_VALUE)] * 100
            )
            self.nand_df.to_csv(self.nand_path)

    def write(self, address: int, data: str) -> None:
        self.nand_df = pd.read_csv(self.nand_path)
        self.nand_df.loc[address, "Data"] = data
        if os.path.exists(self.nand_path):
            os.remove(self.nand_path)
        self.nand_df["Data"].to_csv(self.nand_path, index_label="index")

    def read(self, address: int) -> None:
        self.nand_df = pd.read_csv(self.nand_path)
        if os.path.exists(self.result_path):
            os.remove(self.result_path)
        result_df = pd.DataFrame(
            data=[self.nand_df.loc[address, "Data"]], columns=["Data"]
        )
        result_df = result_df.replace("\n", "")
        result_df.to_csv(self.result_path, index_label="index")
