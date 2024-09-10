# dbtx
Cross-platform dbt runner. Python not required.

Why use this:
- Never think about managing dbt version conflicts again.
- Determines your dbt dialect and version automatically based on your `dbt_project.yml` and `profiles.yml`
- New users don't have to install python (which can be difficult) to get started with dbt.
- Much faster installs thanks to uv and uvx.

# Installation

Install uv with our standalone installers, or from [PyPI](https://pypi.org/project/uv/):

## On macOS and Linux.
```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh && uv tool install dbtx 
```

## On Windows.
```console
$ powershell -c "irm https://astral.sh/uv/install.ps1 | iex ; if ($?) { uv tool install dbtx }"
```

# With pip.
```console
$ pip install dbtx
```

# Usage
1. Make sure you have `require-dbt-version` set in your `dbt_project.yml` file. Otherwise, defaults to the latest version.
2. Just replace `dbtx` where you would use `dbt`. That's it!




