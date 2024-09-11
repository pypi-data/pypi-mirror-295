"""Collection of useful commands for `pytest-neos` management.

To view a list of available commands:

$ invoke --list
"""

import invoke


@invoke.task
def install(context):
    """Install production requirements for `pytest-neos`."""
    context.run("uv sync")


@invoke.task
def install_dev(context):
    """Install development requirements for `pytest-neos`."""
    context.run("uv sync --extra dev")
    context.run("uv run pre-commit install")


@invoke.task
def check_style(context):
    """Run style checks."""
    context.run("ruff .")


@invoke.task
def tests(context):
    """Run pytest unit tests."""
    context.run("pytest -x -s")


@invoke.task
def tests_debug(context):
    """Run pytest unit tests with debug logs."""
    context.run("pytest -x -s -o log_cli=1 -o log-cli-level=DEBUG")


@invoke.task
def tests_coverage(context, output="term-missing"):
    """Run pytest unit tests with coverage.

    Coverage when plugins are involved gets funky, without this coverage is reported at 50-60% instead of 100%
    https://pytest-cov.readthedocs.io/en/latest/plugins.html
    """
    context.run(
        f"COV_CORE_SOURCE=pytest_neos COV_CORE_CONFIG=pyproject.toml COV_CORE_DATAFILE=.coverage.eager pytest --cov=pytest_neos -x --cov-report={output}",
    )


@invoke.task
def release(context):
    """Bump to next X.Y.Z version."""
    context.run("changelog generate")


@invoke.task
def set_common_dev(context):
    """Use editable version of `neos-common`."""
    context.run("uv remove neos-common")
    context.run("uv add ../neos-platform-common --editable --extra auth")


@invoke.task
def unset_common_dev(context):
    """Use published version of `neos-common`."""
    context.run("uv remove neos-common")
    context.run("uv add neos-common[auth]")
