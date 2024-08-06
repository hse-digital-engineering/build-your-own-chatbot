# example-project-with-rye

An example python AI project, testing out some best practices for python development

- using [rye](https://rye.astral.sh/) as a build tool,
- using [pyright](https://microsoft.github.io/pyright/#/) for static type checking and linting,
- and [pre-commit](https://pre-commit.com/) for pre-commit checks.

To be used as a template.



## Getting started

the repo contains a sample package called `example_project_with_rye`.

Replace it with our own one:

1. Rename the package at `src/`
2. Update the test at `tests/`
3. Update the `pyproject.toml`:
   1.   ```
        [project]
        name = "example-project-with-rye"
        version = "0.1.0"
        description = "Add your description here"
        authors = [
            { name = "Max", email = "Max@example-project-with-rye.com" }
        ]
        ```
    2.  ```
        [project.scripts]
        "example-project-with-rye" = "example_project_with_rye:main"
        ```
    3.  ```
        [tool.hatch.build.targets.wheel]
        packages = ["src/example_project_with_rye"]
        ```


## Features

- uses [rye](https://rye.astral.sh/) as a build tool.
    - pyproject.toml is used to configure rye.
    - .python-version is used to specify the python version.
    - requirements.lock and requirements-dev.lock are automatically generated.
- uses [pytest](https://docs.pytest.org/) for testing.
    - test files are located in the `tests` directory.
    - test files are named `test_*.py`.
- uses [pyright](https://microsoft.github.io/pyright/) for static type checking and linting.
- uses ruff /rye as linter.
    - settings are configure in the `[tool.ruff]` section of the `pyproject.toml` file.
- uses [pre-commit](https://pre-commit.com/) for pre-commit checks.
    - pre-commit checks are configured in the `.pre-commit-config.yaml` file.
    - pre-commit checks are run automatically before each commit.
    - includes: lint, type-check (pyright), and detect-secrets.

## Installation

Follow these steps to install the required tools to run this program:

* Install [rye](https://rye.astral.sh/guide/installation/).
* Run following command to install the required dependencies in a virtual environment:
    ```sh
    rye sync
    ```
* ALTERNATIVE: Install the dependencies manually:
    ```sh
    pip install -r requirements.lock
    pip install -r requirements-dev.lock
    ```

* Configure the Python Interpreter of your IDE to use the `.venv` environment.
* Duplicate the `.env.example` file and rename it to `.env`. Fill in the required fields.

### PyCharm Configuration

* In Pycharm, mark the `src` directory as source root:
    * Right-click on the `src` directory -> Mark Directory as -> Sources Root
* In Pycharm, mark the `tests` directory as test root:
    * Right-click on the `tests` directory -> Mark Directory as -> Test Sources Root
* When running tests, make sure that pytest is configured as test runner in your IDE.
    * For PyCharm: Settings -> Tools -> Python Integrated Tools -> Testing -> Default test runner -> pytest
    * You will need to delete any existing run configurations for tests and re-create them!
* Plugins:
    * Install the 'pyright Language Server' plugin for PyCharm.
      Under Settings -> Tools -> Pyright LS (Local),
      set the path to the pyright-langserver executable,
      e.g.:.venv\Scripts\pyright-langserver.exe

## Usage

...

<details>
<summary> <b><span style="font-size: large; ">Additional developer commands (Click to expand)</span></b> </summary>

#### Adding and Updating dependencies:

* Add langchain as regular dependency
    ```sh
    rye add langchain
    ```

* Add pytest as dev dependency
    ```sh
    rye add pytest --dev
    ```


* Update specific package:
    ```sh
    rye sync --update langchain
    ```


* Update all packages:
    ```sh
    rye sync --update-all
    ```

* Update rye itself:
    ```sh
    rye self update
    ```

#### Formatting, Linting and Type Checking:

* Find all lint errors, auto fix some:
    ```sh
    rye lint --fix
    ```

* Static type and syntax checking:
    ```sh
    pyright
    ```

* Auto-format all files:
    ```sh
    rye fmt
    ```

#### Pre-Commit Checks:

* Install pre-commit checks, that will be run automatically before each commit:
    ```sh
    # (only for staged files)
    pre-commit install --hook-type pre-commit
    ```

* Manually run configured pre-commit checks on the currently staged files:
    ```sh
    pre-commit run
    ```

* Manually run configured pre-commit checks, on all files, including unstaged:
    ```sh
    pre-commit run --all-files
    ```

* Update all configured pre-commit hook scripts to their newest versions:

```sh
pre-commit autoupdate
```

</details>
