import unittest
import sys 
import os 
from unittest.mock import patch, mock_open, MagicMock
from fawern.chat_python import ChatPython  

class TestChatPython(unittest.TestCase):

    @patch('fawern.chat_python.Groq')
    def setUp(self, MockGroq):
        self.mock_client = MockGroq.return_value
        self.chat_python = ChatPython()

    def test_generate_code(self):
        self.mock_client.chat.completions.create.return_value = [
            MagicMock(choices=[MagicMock(delta=MagicMock(content="def sum_list(lst):\n    return sum(lst)\n"))])
        ]
        
        code = self.chat_python.generate_code("Bana [1, 2, 3, 4, 5] listesi verildi. Bu listenin elemanlarını toplayan bir fonksiyon yazın.")
        self.assertEqual(code.strip(), "def sum_list(lst):\n    return sum(lst)")

    def test_remove_python_prefix(self):
        code_with_prefix = "python\ndef sum_list(lst):\n    return sum(lst)"
        cleaned_code = self.chat_python.remove_python_prefix(code_with_prefix)
        self.assertEqual(cleaned_code.strip(), "def sum_list(lst):\n    return sum(lst)")

    @patch('fawern.chat_python.os.path.join', return_value="test_code.py")
    @patch('builtins.open', new_callable=mock_open)
    def test_write_code_to_file(self, mock_open, mock_path_join):
        self.chat_python.generated_code = "def sum_list(lst):\n    return sum(lst)"
        self.chat_python.file_name = "test_code.py"
        
        self.chat_python.write_code_to_file("./")
        
        mock_open.assert_called_once_with("test_code.py", "w")
        
        mock_open().write.assert_called_once_with("def sum_list(lst):\n    return sum(lst)")

    @patch('fawern.chat_python.subprocess.run')
    def test_run_generated_code(self, mock_run):
        mock_run.return_value.stdout = "15\n"
        self.chat_python.file_name = "test_code.py"
        
        output = self.chat_python.run_generated_code()
        self.assertEqual(output.strip(), "15")

if __name__ == "__main__":
    unittest.main()
