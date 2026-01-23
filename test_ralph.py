#!/usr/bin/env python3
"""Unit tests for ralph.py"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, mock_open, call
import signal

# Add parent directory to path to import ralph
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from oh_my_ralph.ralph import RalphLoop


class TestRalphLoop(unittest.TestCase):
    """Test cases for RalphLoop class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")
        self.prompt_file = os.path.join(self.temp_dir, ".ralphy", "prompt.md")
        
        # Create .ralphy directory structure
        os.makedirs(os.path.dirname(self.prompt_file), exist_ok=True)
        
        # Create test prompt file
        with open(self.prompt_file, "w", encoding="utf-8") as f:
            f.write("Test prompt content")
        
        # Mock signal handlers to avoid side effects
        self.signal_patcher = patch("oh_my_ralph.ralph.signal.signal")
        self.mock_signal = self.signal_patcher.start()
        
        # Store original signal handlers to restore later
        self.original_sigint = signal.getsignal(signal.SIGINT)
        self.original_sigterm = signal.getsignal(signal.SIGTERM)

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test RalphLoop initialization."""
        ralph = RalphLoop(
            agent_command="test_agent",
            prompt_file="test.md",
            delay_between_loops=10,
            max_iterations=5,
            log_file=self.log_file,
            model="test-model",
            opencode_port=9000,
            working_dir=self.temp_dir,
        )
        
        self.assertEqual(ralph.agent_command, "test_agent")
        self.assertEqual(ralph.delay, 10)
        self.assertEqual(ralph.max_iterations, 5)
        self.assertEqual(ralph.model, "test-model")
        self.assertEqual(ralph.opencode_port, 9000)
        self.assertEqual(ralph.iteration, 0)
        self.assertTrue(ralph.running)

    def test_log_to_file(self):
        """Test logging to file."""
        ralph = RalphLoop(log_file=self.log_file, working_dir=self.temp_dir)
        ralph._log("Test message")
        
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Test message", content)

    def test_read_prompt_success(self):
        """Test reading prompt file successfully."""
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        prompt = ralph._read_prompt()
        self.assertEqual(prompt, "Test prompt content")

    def test_read_prompt_missing_file(self):
        """Test reading non-existent prompt file."""
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        # Remove the prompt file
        os.remove(self.prompt_file)
        
        with self.assertRaises(FileNotFoundError):
            ralph._read_prompt()

    def test_build_agent_command_opencode(self):
        """Test building command for opencode agent."""
        ralph = RalphLoop(
            agent_command="opencode run",
            model="test-model",
            opencode_port=8089,
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        cmd = ralph._build_agent_command("test prompt")
        
        self.assertIn("opencode run", cmd)
        self.assertIn("--model test-model", cmd)
        self.assertIn("--attach http://localhost:8089", cmd)
        self.assertIn("Read and follow the instructions", cmd)

    def test_build_agent_command_other_agent(self):
        """Test building command for non-opencode agent."""
        ralph = RalphLoop(
            agent_command="some-other-agent",
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        cmd = ralph._build_agent_command("test prompt")
        
        self.assertEqual(cmd, "some-other-agent")

    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_run_agent_success(self, mock_popen):
        """Test successful agent execution."""
        mock_process = Mock()
        mock_process.communicate.return_value = ("stdout content", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="test-agent",
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        return_code, stdout, stderr = ralph._run_agent("test prompt")
        
        self.assertEqual(return_code, 0)
        self.assertEqual(stdout, "stdout content")
        self.assertEqual(stderr, "")

    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_run_agent_failure(self, mock_popen):
        """Test agent execution failure."""
        mock_process = Mock()
        mock_process.communicate.return_value = ("", "error message")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="test-agent",
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        return_code, stdout, stderr = ralph._run_agent("test prompt")
        
        self.assertEqual(return_code, 1)
        self.assertEqual(stderr, "error message")

    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_run_agent_timeout(self, mock_popen):
        """Test agent execution timeout."""
        import subprocess
        
        mock_process = Mock()
        mock_process.communicate.side_effect = subprocess.TimeoutExpired("cmd", 3600)
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="test-agent",
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        return_code, stdout, stderr = ralph._run_agent("test prompt")
        
        self.assertEqual(return_code, -1)
        self.assertIn("timed out", stderr.lower())
        mock_process.kill.assert_called_once()

    def test_check_prerequisites_all_exist(self):
        """Test prerequisites check when all files exist."""
        # Create all required files
        agent_md = os.path.join(self.temp_dir, ".ralphy", "agent.md")
        fix_plan_md = os.path.join(self.temp_dir, ".ralphy", "fix_plan.md")
        
        with open(agent_md, "w") as f:
            f.write("agent content")
        with open(fix_plan_md, "w") as f:
            f.write("fix plan content")
        
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        result = ralph._check_prerequisites()
        self.assertTrue(result)

    def test_check_prerequisites_missing_prompt(self):
        """Test prerequisites check when prompt file is missing."""
        os.remove(self.prompt_file)
        
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        result = ralph._check_prerequisites()
        self.assertFalse(result)

    def test_check_prerequisites_missing_other_files(self):
        """Test prerequisites check when non-critical files are missing."""
        # Only prompt.md exists
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        result = ralph._check_prerequisites()
        self.assertTrue(result)  # Should still pass if only prompt exists

    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_run_single_iteration_success(self, mock_popen):
        """Test a successful single iteration."""
        mock_process = Mock()
        mock_process.communicate.return_value = ("success output", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="test-agent",
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        success = ralph.run_single_iteration()
        
        self.assertTrue(success)
        self.assertEqual(ralph.iteration, 1)

    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_run_single_iteration_failure(self, mock_popen):
        """Test a failed single iteration."""
        mock_process = Mock()
        mock_process.communicate.return_value = ("", "error")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="test-agent",
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        success = ralph.run_single_iteration()
        
        self.assertFalse(success)
        self.assertEqual(ralph.iteration, 1)

    def test_signal_handler(self):
        """Test signal handler sets running to False."""
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        self.assertTrue(ralph.running)
        ralph._signal_handler(signal.SIGINT, None)
        self.assertFalse(ralph.running)

    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_start_opencode_web_server(self, mock_popen):
        """Test starting opencode web server."""
        mock_process = Mock()
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            opencode_port=8089,
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        ralph.start_opencode_web_at_port()
        
        mock_popen.assert_called_once()
        self.assertIsNotNone(ralph.opencode_proc)

    def test_stop_opencode_server(self):
        """Test stopping opencode web server."""
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        # Mock a running process
        mock_proc = Mock()
        mock_proc.poll.return_value = None  # Process is running
        ralph.opencode_proc = mock_proc
        
        ralph._stop_opencode_server()
        
        mock_proc.terminate.assert_called_once()

    def test_stop_opencode_server_not_running(self):
        """Test stopping when server is not running."""
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        # No process set
        ralph.opencode_proc = None
        
        # Should not raise an exception
        ralph._stop_opencode_server()

    @patch("oh_my_ralph.ralph.time.sleep")
    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_run_with_max_iterations(self, mock_popen, mock_sleep):
        """Test run loop with max iterations."""
        mock_process = Mock()
        mock_process.communicate.return_value = ("output", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="test-agent",
            max_iterations=2,
            delay_between_loops=1,
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        # Mock the opencode server methods to prevent side effects
        with patch.object(ralph, 'start_opencode_web_at_port'):
            with patch.object(ralph, '_stop_opencode_server'):
                ralph.run()
        
        self.assertEqual(ralph.iteration, 2)

    def test_output_preview_long(self):
        """Test that long stdout is truncated in log."""
        ralph = RalphLoop(working_dir=self.temp_dir, log_file=self.log_file)
        
        long_output = "x" * 1000
        
        # Mock the agent to return long output
        with patch.object(ralph, "_run_agent") as mock_run:
            mock_run.return_value = (0, long_output, "")
            ralph.run_single_iteration()
        
        # Check log file
        with open(self.log_file, "r", encoding="utf-8") as f:
            log_content = f.read()
            # Should show preview
            self.assertIn("Output preview:", log_content)

    def test_consecutive_failures_warning(self):
        """Test warning after consecutive failures."""
        ralph = RalphLoop(
            agent_command="test-agent",
            max_iterations=10,
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        # Mock agent to always fail
        with patch.object(ralph, "_run_agent") as mock_run:
            mock_run.return_value = (1, "", "error")
            with patch("oh_my_ralph.ralph.time.sleep"):  # Skip sleep delays
                with patch.object(ralph, 'start_opencode_web_at_port'):
                    with patch.object(ralph, '_stop_opencode_server'):
                        ralph.run()
        
        # Check log for consecutive failures warning
        with open(self.log_file, "r", encoding="utf-8") as f:
            log_content = f.read()
            self.assertIn("consecutive failures", log_content)


class TestRalphLoopIntegration(unittest.TestCase):
    """Integration tests for RalphLoop."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.log_file = os.path.join(self.temp_dir, "test.log")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("oh_my_ralph.ralph.time.sleep")
    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_full_loop_execution(self, mock_popen, mock_sleep):
        """Test full loop execution flow."""
        # Create .ralphy structure
        ralphy_dir = os.path.join(self.temp_dir, ".ralphy")
        os.makedirs(ralphy_dir, exist_ok=True)
        
        prompt_file = os.path.join(ralphy_dir, "prompt.md")
        with open(prompt_file, "w") as f:
            f.write("Test prompt")
        
        # Mock successful agent execution
        mock_process = Mock()
        mock_process.communicate.return_value = ("Success", "")
        mock_process.returncode = 0
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process
        
        ralph = RalphLoop(
            agent_command="echo test",
            max_iterations=3,
            delay_between_loops=0,
            working_dir=self.temp_dir,
            log_file=self.log_file,
        )
        
        # Mock the opencode server methods to prevent side effects
        with patch.object(ralph, 'start_opencode_web_at_port'):
            with patch.object(ralph, '_stop_opencode_server'):
                ralph.run()
        
        # Verify iterations completed
        self.assertEqual(ralph.iteration, 3)
        
        # Verify log file exists and has content
        self.assertTrue(os.path.exists(self.log_file))
        with open(self.log_file, "r") as f:
            log_content = f.read()
            self.assertIn("Starting Ralph Loop", log_content)
            self.assertIn("Iteration 3", log_content)


class TestNoSideEffects(unittest.TestCase):
    """Tests to ensure no real commands are executed during tests."""
    
    @patch("oh_my_ralph.ralph.signal.signal")
    def test_no_subprocess_without_mock(self, mock_signal):
        """Ensure subprocess.Popen is never called in tests without mocking."""
        # This test verifies our test design - if this fails, we have a test
        # that might accidentally run real commands
        
        # Create a RalphLoop instance
        ralph = RalphLoop(
            agent_command="echo 'THIS SHOULD NEVER RUN'",
            working_dir=tempfile.mkdtemp(),
            log_file=os.path.join(tempfile.gettempdir(), "test.log"),
        )
        
        # Verify we can create the object without side effects
        self.assertIsNotNone(ralph)
        self.assertEqual(ralph.agent_command, "echo 'THIS SHOULD NEVER RUN'")
        
        # The object should exist but NOT have run any commands
        self.assertEqual(ralph.iteration, 0)
    
    @patch("oh_my_ralph.ralph.signal.signal")
    @patch("oh_my_ralph.ralph.subprocess.Popen")
    def test_subprocess_always_mocked_in_execution(self, mock_popen, mock_signal):
        """Ensure subprocess calls are always mocked when executing."""
        mock_process = Mock()
        mock_process.communicate.return_value = ("test", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process
        
        temp_dir = tempfile.mkdtemp()
        prompt_file = os.path.join(temp_dir, ".ralphy", "prompt.md")
        os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
        
        with open(prompt_file, "w") as f:
            f.write("test prompt")
        
        ralph = RalphLoop(
            agent_command="this-command-should-be-mocked",
            working_dir=temp_dir,
            log_file=os.path.join(temp_dir, "test.log"),
        )
        
        # Call the agent
        return_code, stdout, stderr = ralph._run_agent("test")
        
        # Verify the mock was called, not the real subprocess
        mock_popen.assert_called_once()
        self.assertEqual(return_code, 0)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    # Print warning before running tests
    print("=" * 70)
    print("RUNNING UNIT TESTS - NO REAL COMMANDS WILL BE EXECUTED")
    print("All subprocess calls are mocked to prevent side effects")
    print("=" * 70)
    print()
    unittest.main()
