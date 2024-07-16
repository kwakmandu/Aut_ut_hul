from abc import ABC, abstractmethod


class StorageDeviceInterface(ABC):
    @abstractmethod
    def write(self, addr: int, data: str) -> None:
        pass

    @abstractmethod
    def read(self, address: int) -> None:
        pass
