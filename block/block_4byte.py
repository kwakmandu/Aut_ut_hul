from block.block_interface import BlockInterface


class Block4Byte(BlockInterface):
    def __init__(self, address: int, data: str):
        self.__address = address
        self.__data = data

    def get_address(self) -> int:
        pass

    def get_data(self) -> str:
        pass
