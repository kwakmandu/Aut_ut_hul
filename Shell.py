class Validate:
    def is_valid_data(self):
        pass

    def is_valid_LBA_addr(self):
        pass

    def command_string_parser(self):
        pass


class Shell:

    def __init__(self):
        pass

    def run(self):

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
        pass

    def read(self, address: int) -> None:
        pass

    def exit(self):
        pass

    def help(self):
        pass

    def fullwrite(self):
        pass

    def fullread(self):
        pass


if __name__ == "__main__":
    shell = Shell()
    shell.run()
