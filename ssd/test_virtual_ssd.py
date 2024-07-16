from unittest import TestCase
from virtual_ssd import VirtualSSD


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
        data_init_value = "0x00000000"

        # act
        ssd.read(addr_will_be_read)

        # result.txt read
        file_path = "result.txt"
        with open(file_path, "r", encoding="utf-8") as file:
            actual = file.readline().strip()

        # assert
        self.assertEqual(data_init_value, actual)

    def test_virtual_ssd_read_case_적은곳(self) -> None:
        # arrange
        ssd = VirtualSSD()
        addr_will_be_write_read = 35
        data_will_be_write = "0xAAAABBBB"

        # act
        ssd.write(addr_will_be_write_read, data_will_be_write)
        ssd.read(addr_will_be_write_read)

        # result.csv read
        file_path = "result.txt"
        with open(file_path, "r", encoding="utf-8") as file:
            actual = file.readline().strip()

        # assert
        self.assertEqual(data_will_be_write, actual)
