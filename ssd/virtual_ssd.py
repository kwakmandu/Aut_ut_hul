from block.block_4byte import Block4Byte
from ssd.storage_device_interface import StorageDeviceInterface


class VirtualSSD(StorageDeviceInterface):
    def write(self, block: Block4Byte) -> None:
        pass

    def read(self, address: int) -> None:
        pass
