from unittest import TestCase
from unittest.mock import Mock, patch

from Shell import Shell
from ssd import VirtualSSD

ADDRESS = 3
DATA = "0x1298CDEF"


class TestShell(TestCase):

    def setUp(self):
        self.shell = Shell()

    @patch("builtins.input", side_effect=["write 3 0x1298CDEF", "exit"])
    @patch.object(VirtualSSD, "write")
    def test_write_command(self, mock_write, mock_input) -> None:
        self.shell.run()
        mock_write.assert_called_with(3, "0x1298CDEF")

    # def test_read(self) -> None:
    #     self.storage_device.read(ADDRESS)
    #     print(self.storage_device.read.call_count())
