class Helper:
    def __init__(self) -> None:
        self.__help_information = [
            "Available commands:",
            "  write <LBA> <value>  - Write value to the specified LBA",
            "  read <LBA>           - Read value from the specified LBA",
            "  fullwrite <value>    - Write value to all LBAs",
            "  fullread             - Read values from all LBAs",
            "  exit                 - Exit the shell",
            "  help                 - Show this help message",
        ]

    def get_help_information(self) -> list[str]:
        return self.__help_information
