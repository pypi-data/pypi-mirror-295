import subprocess

DBT_PROJECT_DIR = "tests/jaffle_shop_duckdb"
BASE_ENV = {"DBT_PROJECT_DIR": DBT_PROJECT_DIR}


def run_cli(command: list[str], env: dict[str, str] | None = BASE_ENV):
    env_str = " ".join([f"{k}={v}" for k, v in env.items()]) if env else ""
    return subprocess.run(
        f"{env_str} python main.py {' '.join(command)}",
        capture_output=True,
        shell=True,
        text=True,
    )


def test_runner_fails_in_wrong_dir():
    res = run_cli(["--version"], None)
    assert res.returncode == 1
    assert "Could not find profiles.yml file." in res.stderr


def test_runner_fails_no_command():
    res = run_cli([], None)
    assert res.returncode == 1
    assert "No dbt command provided" in res.stderr


def test_runner_succeeds_in_correct_dir():
    res = run_cli(["--version"])
    assert res.returncode == 0
    assert "duckdb" in res.stdout
