from ssd.storage_device_interface import StorageDeviceInterface
from ssd.virtual_ssd import VirtualSSD


class Validate:
    def is_valid_data(self) -> None:
        pass

    def is_valid_LBA_addr(self) -> None:
        pass

    def command_string_parser(self) -> None:
        pass


class Shell:

    def __init__(self) -> None:
        self.ssd: StorageDeviceInterface = VirtualSSD()

    def run(self) -> None:

        while True:
            inputs = input().split(" ")
            if inputs[0] == "ssd" and inputs[1] == "W":
                self.write(inputs[2], inputs[3])

            if inputs[0] == "ssd" and inputs[1] == "R":
                self.read(inputs[2])

            elif inputs[0] == "exit":
                break

            elif inputs[0] == "help":
                pass

            elif inputs[0] == "fullwrite":
                pass

            elif inputs[0] == "fullread":
                pass

    def write(self, address: int, data: str) -> None:
        self.ssd.write(address, data)

    def read(self, address: int) -> None:
        print(self.ssd.read(address))

    def exit(self) -> None:
        pass

    def help(self) -> None:
        pass

    def fullwrite(self) -> None:
        pass

    def fullread(self) -> None:
        pass


if __name__ == "__main__":
    shell = Shell()
    shell.run()
