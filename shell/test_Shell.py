from unittest import TestCase, skip
from unittest.mock import patch

from Shell.shell import Shell


class TestShell(TestCase):
    @skip
    def setUp(self):
        self.shell = Shell()

    @skip
    @patch("builtins.input", side_effect=["exit"])
    def test_exit(self, mock_input):
        self.shell.run()
        self.assertFalse(self.shell.is_run)

    @skip
    @patch("builtins.input", side_effect=["help", "exit"])
    def test_help_command(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("Available commands:")
            mock_print.assert_any_call(
                "  write <LBA> <value>  - Write value to the specified LBA"
            )
            mock_print.assert_any_call(
                "  read <LBA>           - Read value from the specified LBA"
            )
            mock_print.assert_any_call(
                "  fullwrite <value>    - Write value to all LBAs"
            )
            mock_print.assert_any_call(
                "  fullread             - Read values from all LBAs"
            )
            mock_print.assert_any_call("  exit                 - Exit the shell")
            mock_print.assert_any_call(
                "  help                 - Show this help message"
            )
