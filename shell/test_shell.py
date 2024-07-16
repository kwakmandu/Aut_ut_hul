from unittest import TestCase, skip
from unittest.mock import Mock, patch

from shell import Shell
from ssd.virtual_ssd import VirtualSSD


class TestShell(TestCase):

    def setUp(self):
        self.shell = Shell()

    @patch("builtins.input", side_effect=["ssd W 3 0x1298CDEF", "exit"])
    @patch.object(VirtualSSD, "write")
    def test_write_command(self, mock_write, mock_input) -> None:
        self.shell.run()
        mock_write.assert_called_with("3", "0x1298CDEF")

    @patch("builtins.input", side_effect=["ssd R 3", "exit"])
    @patch.object(VirtualSSD, "read", return_value="0x1298CDEF")
    def test_read_command(self, mock_read, mock_input) -> None:
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_read.assert_called_with("3")
            mock_print.assert_any_call("0x1298CDEF")

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
