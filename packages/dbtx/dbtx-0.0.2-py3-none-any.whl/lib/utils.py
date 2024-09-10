import os
from contextlib import contextmanager


def adjust_path(path: str) -> str:
    return os.path.abspath(os.path.expanduser(path))


@contextmanager
def set_env_var(key, value):
    # Save the original value (if any)
    original_value = os.environ.get(key)

    # Set the new environment variable
    os.environ[key] = value

    try:
        # Yield control to the context
        yield
    finally:
        # Restore the original value (or delete if there was no original value)
        if original_value is None:
            del os.environ[key]
        else:
            os.environ[key] = original_value


from contextlib import contextmanager


@contextmanager
def cd(path):
    # Save the current working directory
    original_directory = os.getcwd()

    try:
        # Change to the new working directory
        os.chdir(path)
        yield
    finally:
        # Restore the original working directory
        os.chdir(original_directory)
