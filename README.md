<div align="center">
    <h1>oh-my-ralph: Ralph Wiggum Loop Orchestrator</h1>
  <p>
    <a href="https://pypi.org/project/oh-my-ralph/" target="_blank"><img src="https://img.shields.io/pypi/v/oh-my-ralph" alt="PyPI"></a>
    <a href="https://pepy.tech/project/oh-my-ralph" target="_blank"><img src="https://static.pepy.tech/badge/oh-my-ralph" alt="Downloads"></a>
    <img src="https://img.shields.io/badge/python-≥3.10-blue" alt="Python">
    <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
  </p>
  <pre>
      ⠀⠀⠀⠀⠀⠀⣀⣤⣶⡶⢛⠟⡿⠻⢻⢿⢶⢦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⡾⡫⢊⠌⡐⢡⠊⢰⠁⡎⠘⡄⢢⠙⡛⡷⢤⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⢪⢋⡞⢠⠃⡜⠀⠎⠀⠉⠀⠃⠀⠃⠀⠃⠙⠘⠊⢻⠦⠀⠀⠀⠀⠀⠀
⠀⠀⢇⡇⡜⠀⠜⠀⠁⠀⢀⠔⠉⠉⠑⠄⠀⠀⡰⠊⠉⠑⡄⡇⠀⠀⠀⠀⠀⠀
⠀⠀⡸⠧⠄⠀⠀⠀⠀⠀⠘⡀⠾⠀⠀⣸⠀⠀⢧⠀⠛⠀⠌⡇⠀⠀⠀⠀⠀⠀
⠀⠘⡇⠀⠀⠀⠀⠀⠀⠀⠀⠙⠒⠒⠚⠁⠈⠉⠲⡍⠒⠈⠀⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠲⣆⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⠉⡹⠤⠶⠁⠀⠀⠀⠈⢦⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⣦⡀⠀⠀⠀⠀⠧⣴⠁⠀⠘⠓⢲⣄⣀⣀⣀⡤⠔⠃⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣜⠀⠈⠓⠦⢄⣀⣀⣸⠀⠀⠀⠀⠁⢈⢇⣼⡁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢠⠒⠛⠲⣄⠀⠀⠀⣠⠏⠀⠉⠲⣤⠀⢸⠋⢻⣤⡛⣄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢡⠀⠀⠀⠀⠉⢲⠾⠁⠀⠀⠀⠀⠈⢳⡾⣤⠟⠁⠹⣿⢆⠀⠀⠀⠀⠀⠀
⠀⢀⠼⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⠈⣧⠀⠀⠀⠀⠀
⠀⡏⠀⠘⢦⡀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⠀⠀⠀
⢰⣄⠀⠀⠀⠉⠳⠦⣤⣤⡤⠴⠖⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢯⣆⠀⠀⠀
⢸⣉⠉⠓⠲⢦⣤⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣠⣼⢹⡄⠀⠀
⠘⡍⠙⠒⠶⢤⣄⣈⣉⡉⠉⠙⠛⠛⠛⠛⠛⠛⢻⠉⠉⠉⢙⣏⣁⣸⠇⡇⠀⠀
⠀⢣⠀⠀⠀⠀⠀⠀⠉⠉⠉⠙⠛⠛⠛⠛⠛⠛⠛⠒⠒⠒⠋⠉⠀⠸⠚⢇⠀⠀
⠀⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠇⢤⣨⠇⠀
⠀⠀⠀⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⢻⡀⣸⠀⠀⠀
⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⠛⠉⠁⠀⠀⠀
⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⢠⢄⣀⣤⠤⠴⠒⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠘⡆⠀⠀⠀⠀⠀
⠀⠀⠀⡎⠀⠀⠀⠀⠀⠀⠀⠀⢷⠀⠀⢸⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀
⠀⠀⢀⡷⢤⣤⣀⣀⣀⣀⣠⠤⠾⣤⣀⡘⠛⠶⠶⠶⠶⠖⠒⠋⠙⠓⠲⢤⣀⠀
⠀⠀⠘⠧⣀⡀⠈⠉⠉⠁⠀⠀⠀⠀⠈⠙⠳⣤⣄⣀⣀⣀⠀⠀⠀⠀⠀⢀⣈⡇
⠀⠀⠀⠀⠀⠉⠛⠲⠤⠤⢤⣤⣄⣀⣀⣀⣀⡸⠇⠀⠀⠀⠉⠉⠉⠉⠉⠉⠁⠀
  Credit: https://emojicombos.com/ralph-wiggum-ascii-art
  </pre>
  
</div>

## Ralph Wiggum Orchestrator

This is a simple orchestrator for <a href="https://venturebeat.com/technology/how-ralph-wiggum-went-from-the-simpsons-to-the-biggest-name-in-ai-right-now" target="_blank">Ralph Wiggum</a> loop invented by <a href="https://ghuntley.com" target="_blank">Geoffrey Huntley</a>.

## Supports 
1. [Claude Code](#using-with-claude-code)
2. [Github Copilot](#using-with-github-copilot-cli)
3. [Opencode](#using-with-opencode)
4. [Amp](#using-with-amp-sourcegraph)
5. Any other tool that you can call from CLI (Experimental)

## Requirements
Python 3.10+

## How to run?

1. Install the package
    ```
    pip install oh-my-ralph
    ```
2. Place a `requirements.md` file with your detailed requirements in your working directory (where you want the software to be built)
3. Choose an AI agent and run the Ralph Loop with the appropriate command below.

## Using with Claude Code

Claude Code offers Anthropic's Claude models with advanced coding capabilities.

**Prerequisites:**
- Install Claude Code: Follow instructions at <a href="https://code.claude.com" target="_blank">https://code.claude.com</a>

```bash
oh-my-ralph --agent "claude -p" --model sonnet --working-dir /path/to/dir/with/requirements
```

**Note:** The `--dangerously-skip-permissions` flag is automatically added to enable all permissions for seamless operation.

## Using with AMP (Sourcegraph)

AMP provides powerful AI assistance with multi-model support and advanced coding capabilities.

**Prerequisites:**
- Install AMP: `npm install -g @sourcegraph/amp@latest` or use `npx --yes @sourcegraph/amp`

```bash
oh-my-ralph --agent "npx --yes @sourcegraph/amp" --model smart --working-dir /path/to/dir/with/requirements
```

**Note:** The `--dangerously-allow-all` flag is automatically added to enable all permissions for seamless operation.

**Features:**
- Multi-model support (Claude Opus 4.6, GPT-5.2, fast models)
- Advanced coding capabilities with subagents and oracle mode
- Seamless integration with development workflows
- Automatic permission handling with `--dangerously-allow-all` flag for uninterrupted operation

## Using with OpenCode

OpenCode is the default agent and provides a web interface for monitoring progress.

```bash
oh-my-ralph --agent "opencode run" --model opencode/glm-4.7-free --start-opencode-web-at-port 8089 --working-dir /path/to/dir/with/requirements
```

**Features:**
- Web dashboard at `http://localhost:8089`
- Supports various OpenCode models
- Real-time progress monitoring
- Automated permission handling for seamless operation

## Using with GitHub Copilot CLI

GitHub Copilot CLI provides powerful AI assistance with access to GitHub's Copilot models.

**Prerequisites:**
- Install GitHub Copilot CLI: <a href="https://docs.github.com/en/copilot/github-copilot-in-the-cli/quickstart" target="_blank">https://docs.github.com/en/copilot/github-copilot-in-the-cli/quickstart</a>

```bash
oh-my-ralph --agent "copilot -p" --model gpt-4 --working-dir /path/to/dir/with/requirements
```

**Note:** The `--yolo` flag is automatically added to enable all permissions for seamless operation.

**Features:**
- Access to GPT-4 and other Copilot models
- Non-interactive execution per iteration
- Seamless integration with GitHub ecosystem
- Automatic permission skipping with `--yolo` flag for uninterrupted automation
- Runs your specified `agent` command in a loop.
- The loop exits when any of the following occur:
    - The command prints `<PROMPT>DONE</PROMPT>`.
    - The maximum number of iterations is reached, configurable via `--max-iterations`.
    - Error occurs for 5 consecutive runs of the loop.
    - You manually stop the process by pressing `Ctrl+C`.

## Development

### Running Tests

Tests are automatically run during the build process. To run tests manually:

#### If you have `pytest` installed

```bash
pytest
```

#### If you don't have `pytest` installed

```bash
python test_ralph.py -v
python test_cli_model_required.py -v
```

All tests must pass before building.

