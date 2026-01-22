#!/usr/bin/env python3
"""
Ralph Loop - AI-driven autonomous software development technique.

This script implements the "Ralph" technique: an infinite loop that runs
an AI coding agent to autonomously build software one task at a time.

Usage:
    python ralph.py [--agent AGENT_CMD] [--prompt PROMPT_FILE] [--delay SECONDS]

Example:
    python ralph.py --agent "npx --yes @sourcegraph/amp" --prompt PROMPT.md
    python ralph.py --agent "opencode run" --prompt PROMPT.md
    python ralph.py --agent "claude" --prompt PROMPT.md
"""

import argparse
import subprocess
import sys
import time
import signal
from pathlib import Path
from datetime import datetime

class RalphLoop:
    """The Ralph autonomous coding loop."""

    def __init__(
        self,
        agent_command: str = "opencode run",
        prompt_file: str = "PROMPT.md",
        delay_between_loops: int = 5,
        max_iterations: int = 0,  # 0 = infinite
        log_file: str = "ralph.log",
        model: str = None,
        # attach: str = None,
        opencode_port: int = 8089,
        working_dir: str = None,
    ):

        self.agent_command = agent_command
        self.prompt_file = Path(prompt_file)
        self.delay = delay_between_loops
        self.max_iterations = max_iterations
        self.log_file = Path(log_file)
        self.iteration = 0
        self.running = True
        self.model = model
        # self.attach = attach
        self.opencode_port = opencode_port
        self.opencode_proc = None
        self.working_dir = working_dir

        # Handle graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print(f"\n[Ralph] Received shutdown signal. Finishing current iteration...")
        self.running = False
        self._stop_opencode_server()

    def start_opencode_web_at_port(self):
        """Start the opencode web server as a subprocess at the specified port."""
        try:
            cmd = f"opencode web --port {self.opencode_port}"
            self._log(f"Starting opencode web server on port {self.opencode_port}...")
            self.opencode_proc = subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except Exception as e:
            self._log(f"Failed to start opencode web server: {e}")
            self.opencode_proc = None

    def _stop_opencode_server(self):
        """Terminate the opencode web server subprocess if running."""
        if self.opencode_proc and self.opencode_proc.poll() is None:
            self._log("Stopping opencode web server...")
            self.opencode_proc.terminate()
            try:
                self.opencode_proc.wait(timeout=5)
            except Exception:
                self.opencode_proc.kill()
            self.opencode_proc = None

    def _log(self, message: str):
        """Log a message to both console and log file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def _read_prompt(self) -> str:
        """Read the prompt file contents."""
        if not self.prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")

        return self.prompt_file.read_text(encoding="utf-8")

    def _run_agent(self, prompt: str) -> tuple[int, str, str]:
        """
        Run the AI agent with the given prompt.
        Returns (return_code, stdout, stderr).
        """
        try:
            agent_cmd = self.agent_command
            uses_opencode = agent_cmd.strip().startswith("opencode run")
            
            if uses_opencode:
                # For opencode, the message must come before flags like -f
                # Build command: opencode run "message" -f file --model model
                if self.model:
                    agent_cmd += f" --model {self.model}"
                # Always attach to the opencode web server at the specified port
                if self.opencode_port:
                    agent_cmd += f" --attach http://localhost:{self.opencode_port}"
                agent_cmd += f' "Read and follow the instructions in the {self.prompt_file}."'
                print(f"Running command: {agent_cmd}")
                process = subprocess.Popen(
                    agent_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = process.communicate(timeout=3600)  # 1 hour timeout
            else:
                print(f"Running command: {agent_cmd}")
                # Other agents may read from stdin
                process = subprocess.Popen(
                    agent_cmd,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = process.communicate(input=prompt, timeout=3600)  # 1 hour timeout
            
            return process.returncode, stdout, stderr

        except subprocess.TimeoutExpired:
            process.kill()
            return -1, "", "Process timed out after 1 hour"
        except Exception as e:
            return -1, "", str(e)

    def _check_prerequisites(self) -> bool:
        """Check that all required files exist."""
        required_files = [self.prompt_file, Path("AGENT.md"), Path("requirements.md")]
        missing = [f for f in required_files if not f.exists()]

        if missing:
            self._log(f"Warning: Missing files: {', '.join(str(f) for f in missing)}")
            # Only prompt file is truly required
            if self.prompt_file in missing:
                return False

        return True

    def run_single_iteration(self) -> bool:
        """
        Run a single iteration of the Ralph loop.
        Returns True if successful, False otherwise.
        """
        self.iteration += 1
        self._log(f"=== Ralph Loop Iteration {self.iteration} ===")

        try:
            # Read the prompt
            prompt = self._read_prompt()
            self._log(f"Read prompt from {self.prompt_file} ({len(prompt)} chars)")

            # Run the agent
            self._log(f"Running agent: {self.agent_command}")
            start_time = time.time()

            return_code, stdout, stderr = self._run_agent(prompt)

            elapsed = time.time() - start_time
            self._log(f"Agent finished in {elapsed:.1f}s with return code {return_code}")

            # Log output summary
            if stdout:
                # Log last 500 chars of stdout
                output_preview =  stdout[-500:] if len(stdout) > 500 else stdout
                self._log(f"Output preview: ...{output_preview}")

            if stderr and return_code != 0:
                self._log(f"Stderr: {stderr[:500]}")

            return return_code == 0

        except FileNotFoundError as e:
            self._log(f"Error: {e}")
            return False
        except Exception as e:
            self._log(f"Unexpected error: {e}")
            return False



    def run(self):
        """Run the Ralph loop until stopped or max iterations reached."""
        # Change to working directory if provided
        if self.working_dir:
            import os
            import sys
            try:
                os.chdir(self.working_dir)
                self._log(f"Changed working directory to: {self.working_dir}")
            except Exception as e:
                self._log(f"Failed to change directory to {self.working_dir}: {e}")
                sys.exit(1)

        self._log("Starting Ralph Loop...")
        self._log(f"Agent command: {self.agent_command}")
        self._log(f"Prompt file: {self.prompt_file}")
        self._log(f"Delay between loops: {self.delay}s")

        # Start opencode web server
        self.start_opencode_web_at_port()

        if not self._check_prerequisites():
            self._log("Prerequisites check failed. Exiting.")
            self._stop_opencode_server()
            return

        consecutive_failures = 0
        max_consecutive_failures = 5

        try:
            while self.running:
                # Check iteration limit
                if self.max_iterations > 0 and self.iteration >= self.max_iterations:
                    self._log(f"Reached max iterations ({self.max_iterations}). Stopping.")
                    break

                success = self.run_single_iteration()

                if success:
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_consecutive_failures:
                        self._log(
                            f"Too many consecutive failures ({consecutive_failures}). "
                            "Consider checking the prompt or agent configuration."
                        )
                        # Don't exit, just warn - Ralph is about eventual consistency

                if self.running:
                    self._log(f"Waiting {self.delay}s before next iteration...")
                    time.sleep(self.delay)
        finally:
            self._stop_opencode_server()

        self._log(f"Ralph Loop stopped after {self.iteration} iterations.")


def main():
    parser = argparse.ArgumentParser(            
        description="Ralph Loop - AI-driven autonomous software development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ralph.py --agent "npx --yes @sourcegraph/amp" --prompt PROMPT.md
  python ralph.py --agent "opencode run" --prompt PROMPT.md
  python ralph.py --agent "aider --yes-always" --prompt PROMPT.md
  python ralph.py --max-iterations 10  # Run only 10 iterations

The Ralph technique works best when:
  - requirements.md contains clear specifications
  - AGENT.md contains build/run instructions
  - PROMPT.md instructs one task per loop
  - fix_plan.md tracks remaining work
        """,
    )

    parser.add_argument(
        "--working-dir",
        type=str,
        default=None,
        help="Working directory to run the agent in (default: current directory)",
    )

    parser.add_argument(
        "--agent",
        "-a",
        default="npx --yes @sourcegraph/amp",
        help="The agent command to run (default: npx --yes @sourcegraph/amp)",
    )

    parser.add_argument(
        "--prompt",
        "-p",
        default="PROMPT.md",
        help="Path to the prompt file (default: PROMPT.md)",
    )

    parser.add_argument(
        "--delay",
        "-d",
        type=int,
        default=5,
        help="Delay in seconds between loop iterations (default: 5)",
    )

    parser.add_argument(
        "--max-iterations",
        "-m",
        type=int,
        default=0,
        help="Maximum number of iterations, 0 for infinite (default: 0)",
    )

    parser.add_argument(
        "--log",
        "-l",
        default="ralph.log",
        help="Log file path (default: ralph.log)",
    )

    parser.add_argument(
        "--model",
        type=str,
        default="ollama/qwen2.5-coder:7b",
        help="Model name to use (if supported by agent, e.g., opencode)",
    )





    parser.add_argument(
        "--start-opencode-web-at-port",
        type=int,
        default=8089,
        help="Port for opencode web server (default: 8089)",
    )

    args = parser.parse_args()



    ralph = RalphLoop(
        agent_command=args.agent,
        prompt_file=args.prompt,
        delay_between_loops=args.delay,
        max_iterations=args.max_iterations,
        log_file=args.log,
        model=args.model,
        opencode_port=args.start_opencode_web_at_port,
        working_dir=args.working_dir,
    )

    ralph.run()


if __name__ == "__main__":
    main()
