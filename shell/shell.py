from shell.commander import CommandExecutor, CommandValidator
from logger.logger import Logger
from shell.script_tester import ScriptTester


class Shell:

    def __init__(self) -> None:
        self.__is_run = False
        self.__command_executor: CommandExecutor = CommandExecutor()
        self.__command_validator: CommandValidator = CommandValidator()
        self.__logger: Logger = Logger()
        self.__script_tester: ScriptTester = ScriptTester(
            self.__command_executor, self.__command_validator
        )

    def run(self) -> None:
        self.__logger.print("User IP:192.XX.XX.XX be connected")
        print("Hello ! Welcome to the Aut ut hul shell !")

        self.__is_run = True
        while self.__is_run:
            try:
                user_inputs = input().split()
                if not self.__command_validator.is_valid_command(user_inputs):
                    print("INVALID COMMAND")
                    self.__logger.print(f'INVALID COMMAND - {" ".join(user_inputs)}')
                    continue
                self.__is_run = self.__command_executor.execute_command(user_inputs)

            except Exception as e:
                self.__logger.print(e)

        self.__logger.print("User IP:192.XX.XX.XX be disconnected")
        print("See you !")

    def run_test_list(self, test_list_file: str) -> None:
        self.__script_tester.run_test_list(test_list_file)
