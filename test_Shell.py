class TestShell(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    @patch("builtins.input", side_effect=["write 3 0x1298CDEF", "exit"])
    @patch.object(StorageDevice, "write")
    def test_write_command(self, mock_write, mock_input):
        self.shell.run()
        mock_write.assert_called_with(3, "0x1298CDEF")

    @patch("builtins.input", side_effect=["read 3", "exit"])
    @patch.object(StorageDevice, "read", return_value="0x1298CDEF")
    @patch.object(StorageDevice, "write_result")
    def test_read_command(self, mock_write_result, mock_read, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_read.assert_called_with(3)
            mock_write_result.assert_called_with("0x1298CDEF")
            mock_print.assert_any_call("0x1298CDEF")

    @patch("builtins.input", side_effect=["fullwrite 0xABCDFFFF", "exit"])
    @patch.object(StorageDevice, "write")
    def test_fullwrite_command(self, mock_write, mock_input):
        self.shell.run()
        self.assertEqual(mock_write.call_count, 100)
        mock_write.assert_any_call(0, "0xABCDFFFF")
        mock_write.assert_any_call(99, "0xABCDFFFF")

    @patch("builtins.input", side_effect=["fullread", "exit"])
    @patch.object(StorageDevice, "read", side_effect=lambda lba: f"0x{lba:08X}")
    def test_fullread_command(self, mock_read, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            self.assertEqual(mock_read.call_count, 100)
            mock_read.assert_any_call(0)
            mock_read.assert_any_call(99)
            mock_print.assert_any_call("LBA 0: 0x00000000")
            mock_print.assert_any_call("LBA 99: 0x00000063")

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

    @patch("builtins.input", side_effect=["unknown_command", "exit"])
    def test_invalid_command(self, mock_input):
        with patch("builtins.print") as mock_print:
            self.shell.run()
            mock_print.assert_any_call("INVALID COMMAND")


if __name__ == "__main__":
    unittest.main()
