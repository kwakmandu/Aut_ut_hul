from Block.block4Byte import Block4Byte
from Ssd.storageDeviceInterface import StorageDeviceInterface


class VirtualSSD(StorageDeviceInterface):
    def write(self, block: Block4Byte) -> None:
        pass

    def read(self, address: int) -> None:
        pass
