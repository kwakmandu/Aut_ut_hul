from unittest import TestCase, skip
from block.block_4byte import Block4Byte
from ssd.virtual_ssd import VirtualSSD

import pandas as pd
import os


class Test(TestCase):
    @skip
    def test_virtual_ssd_write_1(self) -> None:
        # arrange
        ssd = VirtualSSD()
        data_will_be_write = "0xAAAABBBB"
        block_will_be_write = Block4Byte(0, data_will_be_write)
        nand_csv_file_path = "nand.csv"
        if os.path.exists(nand_csv_file_path):
            os.remove(nand_csv_file_path)

        # act
        ssd.write(block_will_be_write)

        # assert
        df = pd.read_csv(
            nand_csv_file_path, delimiter=" ", header=None, names=["Address", "Data"]
        )
        block_list = [
            Block4Byte(row["Address"], row["Data"]) for index, row in df.iterrows()
        ]
        actual = block_list[0].get_data()
        self.assertEqual(data_will_be_write, actual)
