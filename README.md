# Workshop Build your own Chatbot

## Getting started

This project is the project template for the workshop. 

Tools used in the project:

- [rye](https://rye.astral.sh/) as a build tool.
  - pyproject.toml is used to configure rye.
  - .python-version is used to specify the python version.
  - requirements.lock and requirements-dev.lock are automatically generated.
- [pytest](https://docs.pytest.org/) for unit testing.
  - test files are located in the `tests` directory.
  - test files are named `test_*.py`.
- [pyright](https://microsoft.github.io/pyright/) for static type checking and linting.
- [ruff](https://docs.astral.sh/ruff/) as linter.
  - settings are configure in the `[tool.ruff]` section of the `pyproject.toml` file.
- [pre-commit](https://pre-commit.com/) for pre-commit checks.
  - pre-commit checks are configured in the `.pre-commit-config.yaml` file.
  - pre-commit checks are run automatically before each commit.
  - includes: lint, type-check (pyright), and detect-secrets.

### Tool Installation

Follow these steps to install the required tools to run this program:

- Install [rye](https://rye.astral.sh/guide/installation/).
- Run following command to install the required dependencies in a virtual environment:
  ```sh
  rye sync
  ```
- ALTERNATIVE: Install the dependencies manually:

  ```sh
  pip install -r requirements.lock
  pip install -r requirements-dev.lock
  ```

- Configure the Python Interpreter of your vscode to use the `.venv` environment.
- Duplicate the `.env.example` file and rename it to `.env`. Fill in the required fields.

### Update project config

Update the `pyproject.toml`:
   1. ```
      [project]
      description = "Add your description here"
      authors = [
          { name = "Max", email = "Max@example-project-with-rye.com" }
      ]
      ```


## Usage

...

<details>
<summary> <b><span style="font-size: large; ">Additional developer commands (Click to expand)</span></b> </summary>

#### Adding and Updating dependencies:

- Add langchain as regular dependency

  ```sh
  rye add langchain
  ```

- Add pytest as dev dependency

  ```sh
  rye add pytest --dev
  ```

- Update specific package:

  ```sh
  rye sync --update langchain
  ```

- Update all packages:

  ```sh
  rye sync --update-all
  ```

- Update rye itself:
  ```sh
  rye self update
  ```

#### Formatting, Linting and Type Checking:

- Find all lint errors, auto fix some:

  ```sh
  rye lint --fix
  ```

- Static type and syntax checking:

  ```sh
  pyright
  ```

- Auto-format all files:
  ```sh
  rye fmt
  ```

#### Pre-Commit Checks:

- Install pre-commit checks, that will be run automatically before each commit:

  ```sh
  # (only for staged files)
  pre-commit install --hook-type pre-commit
  ```

- Manually run configured pre-commit checks on the currently staged files:

  ```sh
  pre-commit run
  ```

- Manually run configured pre-commit checks, on all files, including unstaged:

  ```sh
  pre-commit run --all-files
  ```

- Update all configured pre-commit hook scripts to their newest versions:

```sh
pre-commit autoupdate
```

</details>
