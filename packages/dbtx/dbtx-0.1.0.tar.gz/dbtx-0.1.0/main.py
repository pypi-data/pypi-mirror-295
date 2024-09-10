import argparse
import subprocess
import sys

from lib.dbt import DBTProject


def dbtx():
    parser = argparse.ArgumentParser(
        description="A command-line tool to run dbt commands with custom configuration",
        add_help=False,
    )

    _, unknown_args = parser.parse_known_args()

    if not unknown_args:
        print("No dbt command provided", file=sys.stderr)
        exit(1)

    project = DBTProject(unknown_args)
    version = project.get_version()
    dialect = project.get_dialect()

    command = f'DO_NOT_TRACK=1 uvx --no-progress --isolated --from "dbt-core{version}" --with dbt-{dialect} dbt {" ".join(unknown_args)}'
    subprocess.run(
        command,
        shell=True,
    )


if __name__ == "__main__":
    dbtx()
