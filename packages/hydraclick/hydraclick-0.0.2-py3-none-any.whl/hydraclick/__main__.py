import sys

import click
import flogging

from hydraclick import hydra_command


@click.group()
def cli():
    """Run command line interface for hydraclick."""
    flogging.setup(allow_trailing_dot=True)


@cli.command(short_help="test_stuff.")
@hydra_command()
def nothing(args, **kwargs):  # noqa: ARG001
    """Test function that does nothing."""


if __name__ == "__main__":
    sys.exit(cli())
