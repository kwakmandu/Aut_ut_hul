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
        addr_will_be_write = 0
        data_will_be_write = "0xAAAABBBB"

        # act
        ssd.write(addr_will_be_write, data_will_be_write)

        # assert
        actual = ssd.nand_df.iloc[addr_will_be_write]
        self.assertEqual(data_will_be_write, actual['Data'])
