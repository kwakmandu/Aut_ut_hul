from unittest import TestCase, skip
from ssd.virtual_ssd import VirtualSSD

import pandas as pd
import os


class Test(TestCase):
    def test_virtual_ssd_write_1(self) -> None:
        # arrange
        ssd = VirtualSSD()
        addr_will_be_write = 0
        data_will_be_write = "0xAAAABBBB"

        # act
        ssd.write(addr_will_be_write, data_will_be_write)

        # assert
        actual = ssd.nand_df.iloc[addr_will_be_write]
        self.assertEqual(data_will_be_write, actual["Data"])

    def test_virtual_ssd_read_case_한번도안적은곳(self) -> None:
        # arrange
        ssd = VirtualSSD()
        addr_will_be_read = 30

        # act
        ssd.read(addr_will_be_read)

        # result.csv read
        actual = pd.read_csv(ssd.result_path)

        # assert
        self.assertEqual("0x00000000", actual.loc[0, "Data"])

    def test_virtual_ssd_read_case_적은곳(self) -> None:
        # arrange
        ssd = VirtualSSD()
        addr_will_be_write_read = 35
        data_will_be_write = "0xAAAABBBB"

        # act
        ssd.write(addr_will_be_write_read, data_will_be_write)
        ssd.read(addr_will_be_write_read)

        # result.csv read
        actual = pd.read_csv(ssd.result_path)

        # assert
        self.assertEqual(data_will_be_write, actual.loc[0, "Data"])
