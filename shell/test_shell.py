from unittest import TestCase, skip, mock
from unittest.mock import Mock, patch, MagicMock, mock_open

from shell import Shell
from ssd.virtual_ssd import VirtualSSD


class TestShell(TestCase):

    def setUp(self):
        self.shell = Shell()

    @patch("subprocess.run")
    def test_write_command(self, mock_subprocess_run):
        address = 3
        data = "0x1298CDEF"
        self.shell.write(address, data)
        mock_subprocess_run.assert_called_with(
            ["python", "../ssd/virtual_ssd.py", "W", str(address), data]
        )

    @patch("subprocess.run")
    @patch("builtins.open", new_callable=mock_open, read_data="1")
    def test_read_command(self, mock_open, mock_subprocess_run):
        address = 3

        mock_open.return_value.read.return_value = "0x1298CDEF"

        with patch("builtins.print") as mock_print:
            self.shell.read(address)
            mock_subprocess_run.assert_called_with(
                ["python", "../ssd/virtual_ssd.py", "R", str(address)]
            )
            mock_open.assert_called_with("result.txt", "r")
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

    @patch("builtins.input", side_effect=["fullwrite 0xABCDFFFF", "exit"])
    @patch.object(VirtualSSD, "write")
    def test_fullwrite_command(self, mock_write, mock_input):
        self.shell.run()
        self.assertEqual(mock_write.call_count, 100)
        mock_write.assert_any_call(0, "0xABCDFFFF")
        mock_write.assert_any_call(99, "0xABCDFFFF")

    @patch("builtins.input", side_effect=["fullread", "exit"])
    @patch.object(VirtualSSD, "read", return_value="0x1298CDEF")
    def test_fullread_command(self, mock_read, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            self.assertEqual(mock_read.call_count, 100)
            mock_read.assert_any_call(0)
            mock_read.assert_any_call(99)
            mock_print.assert_any_call("0x1298CDEF")
