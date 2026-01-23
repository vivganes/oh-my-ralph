
## Ralph Wiggum Orchestrator

This is a simple orchestrator for [Ralph Wiggum](https://venturebeat.com/technology/how-ralph-wiggum-went-from-the-simpsons-to-the-biggest-name-in-ai-right-now) loop invented by [Geoffrey Huntley](https://ghuntley.com).

## Requirements
Python 3.10+

## How to run?

1. Clone this repo
2. Place a `requirements.md` file with your detailed requirements in your working directory (where you want the software to be built)
3. To run ralph using opencode, run the following command:

```bash
oh-my-ralph --agent "opencode run" --model opencode/glm-4.7-free --start-opencode-web-at-port 8089 --working-dir /path/to/dir/with/requirements
```

## Development

### Running Tests

Tests are automatically run during the build process. To run tests manually:

```bash
.\run_tests.bat
```

All 24 tests must pass before building.

### Building the Package

To build the package with mandatory tests:

```bash
.\build.bat
```

This will:
1. Run all tests (build fails if any test fails)
2. Build the package using Python's build module
3. Create distribution files in the `dist\` directory

The build process ensures code quality by enforcing test success before creating distribution packages.