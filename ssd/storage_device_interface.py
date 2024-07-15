from abc import ABC, abstractmethod

from block.block_4byte import Block4Byte


class StorageDeviceInterface(ABC):
    @abstractmethod
    def write(self, addr: int, data: str) -> None:
        pass

    @abstractmethod
    def read(self, address: int) -> None:
        pass
