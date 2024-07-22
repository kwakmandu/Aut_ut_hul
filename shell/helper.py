class Helper:
    def __init__(self) -> None:
        self.__help_information = [
            "Available commands:",
            "  write <LBA> <value>  - Write value to the specified LBA",
            "  read <LBA>           - Read value from the specified LBA",
            "  fullwrite <value>    - Write value to all LBAs",
            "  fullread             - Read values from all LBAs",
            "  erase_range <F_LBA> <L_LBA> - Erase LBAs from F_LBA up to (but not including) L_LBA",
            "  erase <LBA> <size>   - Erase the specified number of LBAs starting from the given LBA",
            "  flush                - Apply all pending write and erase operations from buffer to NAND, then clear the buffer",
            "  exit                 - Exit the shell",
            "  help                 - Show this help message",
        ]

    def get_help_information(self) -> list[str]:
        return self.__help_information
