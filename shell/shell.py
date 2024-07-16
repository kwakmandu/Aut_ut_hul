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
        self.is_run = False
        self.ssd: StorageDeviceInterface = VirtualSSD()
        self.help_information = [
            "Available commands:",
            "  write <LBA> <value>  - Write value to the specified LBA",
            "  read <LBA>           - Read value from the specified LBA",
            "  fullwrite <value>    - Write value to all LBAs",
            "  fullread             - Read values from all LBAs",
            "  exit                 - Exit the shell",
            "  help                 - Show this help message",
        ]

    def run(self) -> None:
        self.is_run = True
        while self.is_run:
            inputs = input().split(" ")
            if inputs[0] == "ssd" and inputs[1] == "W":
                self.write(int(inputs[2]), inputs[3])

            if inputs[0] == "ssd" and inputs[1] == "R":
                self.read(int(inputs[2]))

            elif inputs[0] == "exit":
                self.exit()

            elif inputs[0] == "help":
                self.help()

            elif inputs[0] == "fullwrite":
                pass

            elif inputs[0] == "fullread":
                pass

    def write(self, address: int, data: str) -> None:
        self.ssd.write(address, data)

    def read(self, address: int) -> None:
        print(self.ssd.read(address))

    def exit(self) -> None:
        self.is_run = False

    def help(self) -> None:
        for h_info in self.help_information:
            print(h_info)

    def fullwrite(self) -> None:
        pass

    def fullread(self) -> None:
        pass


if __name__ == "__main__":
    shell = Shell()
    shell.run()
