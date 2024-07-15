from abc import ABC, abstractmethod

from Block.block4Byte import Block4Byte


class StorageDeviceInterface(ABC):
    @abstractmethod
    def write(self, block: Block4Byte) -> None:
        pass

    @abstractmethod
    def read(self, address: int) -> None:
        pass
