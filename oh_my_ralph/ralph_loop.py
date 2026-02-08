import subprocess
import signal
import time
import sys
from pathlib import Path
from datetime import datetime

class RalphLoop:
    """The Ralph autonomous coding loop."""

    def __init__(
        self,
        agent_command: str = "opencode run",
        delay_between_loops: int = 5,
        max_iterations: int = 0,  # 0 = infinite
        log_file: str = "ralph.log",
        model: str = None,
        # attach: str = None,
        opencode_port: int = 8089,
        working_dir: str = None,
    ):
        self.agent_command = agent_command
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
        # Set .ralphy directory and resource file paths
        import os
        base_dir = self.working_dir if self.working_dir else os.getcwd()
        self.ralphy_dir = os.path.join(base_dir, ".ralphy")
        self.agent_md = Path(os.path.join(self.ralphy_dir, "agent.md"))
        self.fix_plan_md = Path(os.path.join(self.ralphy_dir, "fix_plan.md"))
        self.prompt_md = Path(os.path.join(self.ralphy_dir, "prompt.md"))
        # Use prompt_md as the prompt file
        self.prompt_file = self.prompt_md
        # Handle graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        print(f"\n[Ralph] Received shutdown signal. Finishing current iteration...")
        self.running = False
        self._stop_opencode_server()

    def start_opencode_web_at_port(self):
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
        if self.opencode_proc and self.opencode_proc.poll() is None:
            self._log("Stopping opencode web server...")
            self.opencode_proc.terminate()
            try:
                self.opencode_proc.wait(timeout=5)
            except Exception:
                self.opencode_proc.kill()
            self.opencode_proc = None

    def _log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def _read_prompt(self) -> str:
        if not self.prompt_file.exists():
            raise FileNotFoundError(f"Prompt file not found: {self.prompt_file}")
        return self.prompt_file.read_text(encoding="utf-8")

    def _build_agent_command(self, prompt: str) -> str:
        agent_cmd = self.agent_command
        uses_opencode = agent_cmd.strip().startswith("opencode run")
        uses_copilot = "copilot" in agent_cmd
        uses_claude = "claude" in agent_cmd
        uses_amp = "@sourcegraph/amp" in agent_cmd or "amp" in agent_cmd and "--yes" in agent_cmd
        if uses_opencode:
            if self.model:
                agent_cmd += f" --model {self.model}"
            if self.opencode_port:
                agent_cmd += f" --attach http://localhost:{self.opencode_port}"
            agent_cmd += f' "Read and follow the instructions in the file `{self.prompt_file}`."'
        elif uses_copilot or uses_claude or uses_amp:
            if uses_copilot:
                # For copilot, restructure: copilot --model X --yolo -p "prompt"
                base_cmd = agent_cmd.split()[0]  # "copilot"
                flags_part = ""
                if self.model:
                    flags_part += f" --model {self.model}"
                flags_part += " --yolo"
                # Extract any additional flags from original command (like -p)
                additional_flags = " ".join(agent_cmd.split()[1:])  # "-p"
                agent_cmd = f"{base_cmd}{flags_part} {additional_flags}"
            else:
                # For claude and amp, keep the original logic
                if self.model:
                    agent_cmd += f" --model {self.model}"
                if uses_claude:
                    agent_cmd += " --dangerously-skip-permissions"
                elif uses_amp:
                    agent_cmd += " --dangerously-allow-all"
            # For copilot -p, claude -p, and amp, instruct to read the file
            agent_cmd += f' "Read and follow the instructions in the file `{self.prompt_file}`."'
        return agent_cmd

    def _run_agent(self, prompt: str) -> tuple[int, str, str]:
        try:
            agent_cmd = self._build_agent_command(prompt)
            uses_opencode = self.agent_command.strip().startswith("opencode run")
            uses_command_with_prompt_arg = uses_opencode or "copilot" in self.agent_command or "claude" in self.agent_command or "@sourcegraph/amp" in self.agent_command or ("amp" in self.agent_command and "--yes" in self.agent_command)
            print(f"Running command: {agent_cmd}")
            if uses_command_with_prompt_arg:
                process = subprocess.Popen(
                    agent_cmd,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = process.communicate(timeout=3600)
            else:
                process = subprocess.Popen(
                    agent_cmd,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = process.communicate(input=prompt, timeout=3600)
            return process.returncode, stdout, stderr
        except subprocess.TimeoutExpired:
            process.kill()
            return -1, "", "Process timed out after 1 hour"
        except Exception as e:
            return -1, "", str(e)

    def _print_ascii_art(self):
        try:
            import importlib.resources
            files = importlib.resources.files("oh_my_ralph")
            ascii_art_path = files.joinpath("ascii_art.txt")
            with importlib.resources.as_file(ascii_art_path) as art_file:
                with open(art_file, 'r', encoding='utf-8') as f:
                    print(f.read())
        except Exception:
            pass

    def _check_prerequisites(self) -> bool:
        required_files = [self.prompt_md, self.agent_md, self.fix_plan_md]
        missing = [f for f in required_files if not f.exists()]
        if missing:
            self._log(f"Warning: Missing files in .ralphy: {', '.join(str(f) for f in missing)}")
            if self.prompt_md in missing:
                return False
        return True

    def run_single_iteration(self) -> tuple[bool, bool]:
        self.iteration += 1
        self._log(f"=== Ralph Loop Iteration {self.iteration} ===")
        try:
            prompt = self._read_prompt()
            self._log(f"Read prompt from {self.prompt_file} ({len(prompt)} chars)")
            self._log(f"Running agent: {self.agent_command}")
            start_time = time.time()
            return_code, stdout, stderr = self._run_agent(prompt)
            elapsed = time.time() - start_time
            self._log(f"Agent finished in {elapsed:.1f}s with return code {return_code}")
            should_stop = False
            if stdout and "<PROMISE>DONE</PROMISE>" in stdout:
                self._log("=== DETECTED COMPLETION MARKER: <PROMISE>DONE</PROMISE> ===")
                self._log("Agent has indicated work is complete. Stopping Ralph Loop.")
                should_stop = True
            if stdout:
                output_preview =  stdout[-500:] if len(stdout) > 500 else stdout
                self._log(f"Output preview: ...{output_preview}")
            if stderr and return_code != 0:
                self._log(f"Stderr: {stderr[:500]}")
            return (return_code == 0, should_stop)
        except FileNotFoundError as e:
            self._log(f"Error: {e}")
            return (False, False)
        except Exception as e:
            self._log(f"Unexpected error: {e}")
            return (False, False)

    def run(self):
        self._print_ascii_art()
        import os
        import shutil
        base_dir = self.working_dir if self.working_dir else os.getcwd()
        ralphy_dir = os.path.join(base_dir, ".ralphy")
        import importlib.resources
        resource_files = ["agent.md", "fix_plan.md", "prompt.md"]
        resource_paths = []
        for fname in resource_files:
            try:
                files = importlib.resources.files("oh_my_ralph")
                resource_path = files.joinpath(fname)
                if resource_path.is_file():
                    with importlib.resources.as_file(resource_path) as res_path:
                        resource_paths.append(str(res_path))
                else:
                    raise FileNotFoundError(f"{fname} not found in package")
            except (FileNotFoundError, ModuleNotFoundError):
                resource_paths.append(os.path.join(base_dir, fname))
        if not os.path.exists(ralphy_dir):
            os.makedirs(ralphy_dir, exist_ok=True)
            self.copy_resource_files(os, shutil, base_dir, ralphy_dir, resource_files, resource_paths)
        else:
            missing = [fname for fname in resource_files if fname != "prompt.md" and not os.path.exists(os.path.join(ralphy_dir, fname))]
            if missing:
                self._log(f"Warning: .ralphy exists but missing files: {', '.join(missing)}")
                self.copy_resource_files(os, shutil, base_dir, ralphy_dir, missing,
                                         [os.path.join(base_dir, fname) for fname in missing])
            prompt_idx = resource_files.index("prompt.md")
            self.copy_resource_files(os, shutil, base_dir, ralphy_dir, ["prompt.md"], [resource_paths[prompt_idx]])
        if self.working_dir:
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
        time.sleep(5)
        if(self.agent_command.strip().startswith("opencode")):
            self.start_opencode_web_at_port()
        if not self._check_prerequisites():
            self._log("Prerequisites check failed. Exiting.")
            self._stop_opencode_server()
            return
        consecutive_failures = 0
        max_consecutive_failures = 5
        try:
            while self.running:
                if self.max_iterations > 0 and self.iteration >= self.max_iterations:
                    self._log(f"Reached max iterations ({self.max_iterations}). Stopping.")
                    break
                success, should_stop = self.run_single_iteration()
                if should_stop:
                    self._log("Agent signaled completion. Exiting Ralph Loop.")
                    break
                if success:
                    consecutive_failures = 0
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= max_consecutive_failures:
                        self._log(
                            f"Too many consecutive failures ({consecutive_failures}). "
                            "Consider checking the prompt or agent configuration."
                        )
                if self.running:
                    self._log(f"Waiting {self.delay}s before next iteration...")
                    time.sleep(self.delay)
        finally:
            if(self.agent_command.strip().startswith("opencode")):
                self._stop_opencode_server()
        self._log(f"Ralph Loop stopped after {self.iteration} iterations.")

    def copy_resource_files(self, os, shutil, base_dir, ralphy_dir, resource_files, resource_paths):
        for fname, src_path in zip(resource_files, resource_paths):
            dst_path = os.path.join(ralphy_dir, fname)
            print("src_path:", src_path)
            print("dst_path:", dst_path)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                self._log(f"Copied {fname} to {ralphy_dir}")
            else:
                self._log(f"Warning: {fname} not found in {base_dir}, not copied.")
