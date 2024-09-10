# dbtx
Cross-platform dbt runner. Python not required.

Why use this:
- Never think about managing dbt version conflicts again.
- Determines your dbt dialect and version automatically based on your `dbt_project.yml` and `profiles.yml`
- New users don't have to install python (which can be difficult) to get started with dbt.
- Much faster installs thanks to uv and uvx.
- After first run -- when dbt package is downloaded -- speed difference vs. vanilla dbt-core is negligible (<0.2 seconds per command).

# Installation

Install uv with our standalone installers, or from [PyPI](https://pypi.org/project/dbtx/):

### macOS and Linux
```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh && uv tool install dbtx 
```

### Windows
In a PowerShell administrator prompt:
```console
$ powershell -c "irm https://astral.sh/uv/install.ps1 | iex ; uv tool install dbtx"
```

```console
$ $env:PATH = (Join-Path $HOME '.local\bin') + ";$env:PATH"
```

### Within python
```console
$ pip install dbtx
```

# Usage
1. Make sure you have `require-dbt-version` set in your `dbt_project.yml` file. Otherwise, defaults to the latest version.
2. Just replace `dbtx` where you would use `dbt`. That's it!




