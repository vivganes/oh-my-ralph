import sys
import unittest
from unittest.mock import patch
from oh_my_ralph import ralph_cli

class TestCliModelRequired(unittest.TestCase):
    def test_model_argument_required(self):
        test_args = [
            'ralph_cli.py',
            '--agent', 'test-agent',
            '--max-iterations', '1',
        ]
        with patch.object(sys, 'argv', test_args):
            with self.assertRaises(SystemExit) as cm:
                ralph_cli.main()
            self.assertNotEqual(cm.exception.code, 0)
        # argparse prints to stderr
        # Optionally, capture stderr if you want to check the error message

    def test_main_runs_with_all_args(self):
        test_args = [
            'ralph_cli.py',
            '--agent', 'test-agent',
            '--max-iterations', '1',
            '--model', 'test-model'
        ]
        with patch.object(sys, 'argv', test_args):
            with patch('oh_my_ralph.ralph_cli.RalphLoop') as mock_loop:
                instance = mock_loop.return_value
                instance.run = unittest.mock.MagicMock()
                ralph_cli.main()
                mock_loop.assert_called_once()
                instance.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
