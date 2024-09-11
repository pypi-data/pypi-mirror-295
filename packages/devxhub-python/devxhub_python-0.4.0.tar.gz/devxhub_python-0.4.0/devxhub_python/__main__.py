"""Allow devxhub_python to be executable through `python -m devxhub_python`."""

from devxhub_python.cli import main

if __name__ == "__main__":
    main(prog_name="devxhub_python")
