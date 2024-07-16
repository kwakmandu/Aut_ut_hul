import sys
from unittest import TestCase, skip, mock
from unittest.mock import Mock, patch, MagicMock, mock_open

from shell import Shell
from ssd.virtual_ssd import VirtualSSD


class TestShell(TestCase):

    def setUp(self):
        self.shell = Shell()

    @patch("builtins.input", side_effect=["Write 3 0x1298CDEF", "exit"])
    def test_invalid_command_not_allowed_initial_command(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["write X 0x1298CDEF", "exit"])
    def test_invalid_write_command_address_not_numerical(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["read X", "exit"])
    def test_invalid_read_command_address_not_numerical(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["write 100 0x1298CDEF", "exit"])
    def test_invalid_write_command_address_not_in_range(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["write 100 0x00001111 invalid", "exit"])
    def test_invalid_write_command_wrong_args(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["read 100", "exit"])
    def test_invalid_read_command_address_not_in_range(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["write 0 1x1298CDEF", "exit"])
    def test_invalid_write_command_data_initial_not_0x(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["write 0 0x1298CDEF0", "exit"])
    def test_invalid_write_command_data_length_not_10(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["write 0 0x1298CDEX", "exit"])
    def test_invalid_write_command_data_not_in_hex_range(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["fullwrite 1x1298CDEF", "exit"])
    def test_invalid_fullwrite_command_data_initial_not_0x(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["fullwrite 0x00110011 invalid", "exit"])
    def test_invalid_fullwrite_command_wrong_args(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["fullwrite 0x1298CDEF0", "exit"])
    def test_invalid_fullwrite_command_data_length_not_10(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("builtins.input", side_effect=["fullwrite 0x1298CDEX", "exit"])
    def test_invalid_fullwrite_command_data_not_in_hex_range(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")

    @patch("subprocess.run")
    def test_write_command(self, mock_subprocess_run):
        address = "3"
        data = "0x1298CDEF"
        self.shell.write(address, data)
        mock_subprocess_run.assert_called_with(
            [sys.executable, "../ssd/virtual_ssd.py", "W", str(address), data]
        )

    @patch("subprocess.run")
    @patch("builtins.open", new_callable=mock_open, read_data="1")
    def test_read_command(self, mock_open, mock_subprocess_run):
        address = "3"

        mock_open.return_value.read.return_value = "0x1298CDEF"

        with patch("builtins.print") as mock_print:
            self.shell.read(address)
            mock_subprocess_run.assert_called_with(
                [sys.executable, "../ssd/virtual_ssd.py", "R", address]
            )
            mock_open.assert_called_with("../ssd/result.txt", "r")
            mock_open.return_value.read.assert_called_once()
            mock_print.assert_called_with("0x1298CDEF")

    @patch("builtins.input", side_effect=["exit"])
    def test_exit(self, mock_input):
        self.shell.run()
        self.assertFalse(self.shell.is_run)

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

    @patch("subprocess.run")
    def test_fullwrite_command(self, mock_subprocess_run):
        self.shell.fullwrite("0xABCDFFFF")
        self.assertEqual(mock_subprocess_run.call_count, 100)

    @patch("builtins.input", side_effect=["fullread", "exit"])
    @patch("builtins.open", new_callable=mock_open, read_data="1")
    @patch("subprocess.run")
    def test_fullread_command(self, mock_subprocess_run, mock_open, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            self.assertEqual(mock_subprocess_run.call_count, 100)
            self.assertEqual(mock_open.call_count, 100)

    @skip
    @patch("builtins.input", side_effect=["testapp1", "exit"])
    def test_test_app01_테스트(self, mock_input):
        self.shell.run()

    @skip
    @patch("builtins.input", side_effect=["testapp2", "exit"])
    def test_test_app02_테스트(self, mock_input):
        self.shell.run()
