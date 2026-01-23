#!/usr/bin/env python3
"""
CLI entry point for Ralph Loop
"""
import argparse
from .ralph_loop import RalphLoop

def main():
    parser = argparse.ArgumentParser(
        description="Ralph Loop - AI-driven autonomous software development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  oh-my-ralph --agent "npx --yes @sourcegraph/amp"
  oh-my-ralph --agent "opencode run"
  oh-my-ralph --agent "aider --yes-always" 
  oh-my-ralph --max-iterations 10  # Run only 10 iterations

The Ralph Wiggum technique works best when:
  - requirements.md contains clear specifications
  - requirements.md contains a list of features to implement, instead of one big paragraph

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
        default="opencode run",
        help="The agent command to run (e.g., 'opencode run', 'npx --yes @sourcegraph/amp') (default: 'opencode run')",
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
        default=25,
        help="Maximum number of iterations, 0 for infinite (default: 25)",
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
        required=True,
        help="Model name to use (required, e.g., opencode)",
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
