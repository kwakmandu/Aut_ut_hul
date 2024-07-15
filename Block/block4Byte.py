from Block.blockInterface import BlockInterface


class Block4Byte(BlockInterface):
    def __init__(self, address, data):
        super.__init__()
        self.__address = address
        self.__data = data
