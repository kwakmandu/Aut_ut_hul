from unittest import TestCase
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
