from Block.blockInterface import BlockInterface


class Block4Byte(BlockInterface):
    def __init__(self, address: int, data: str):
        super.__init__()
        self.__address = address
        self.__data = data
