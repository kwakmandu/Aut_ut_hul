from abc import ABC, abstractmethod


class StorageDeviceInterface(ABC):
    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def read(self):
        pass
