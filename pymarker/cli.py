import click

from .core import generate_marker, generate_patt, remove_borders
from .exceptions import BlackBorderSizeError, WhiteBorderSizeError
from .utils import echo


@click.group()
def cli():
    """PyMarker CLI"""


@cli.command()
@click.argument("filename")
@click.option("--patt", "-p", is_flag=True, default=False)
@click.option("--marker", "-m", is_flag=True, default=False)
@click.option("--as_string", "-s", is_flag=True, default=False)
@click.option("--black-border-size", "-b", default=20)
@click.option("--white-border-size", "-w", default=3)
@click.option("--inner-border-size", "-i", default=3)
@click.option("--output", "-o", default=None, type=str)
def generate(
    filename,
    patt,
    marker,
    as_string,
    black_border_size,
    white_border_size,
    inner_border_size,
    output,
):
    """Generate marker and/or patt files."""
    echo("-- Starting PyMarker Generator --", silent=as_string)
    if marker or (not patt and not marker):
        echo(f"Generating marker for {filename}", silent=as_string)
        try:
            generate_marker(
                filename,
                black_border_size,
                output,
                white_border_size,
                inner_border_size,
            )
        except BlackBorderSizeError:
            echo(
                "Black border size cannot be less or equal 0 or bigger than 50%",
                silent=as_string,
            )
            return
        except WhiteBorderSizeError:
            echo(
                "White border size cannot be less than 0 or bigger than 50%",
                silent=as_string,
            )
            return

    if patt or (not patt and not marker):
        echo(f"Generating patt for {filename}", silent=as_string)
        echo(generate_patt(filename, output, as_string), silent=not as_string)

    echo("Done.", silent=as_string)


@cli.command()
@click.argument("filename")
@click.option("--output", "-o", default=None, type=str)
def remove(filename, output):
    """Remove borders from marker images."""
    echo(f"Removing generated files for {filename}", silent=False)
    try:
        remove_borders(filename, output)
    except FileNotFoundError:
        echo(f"File {filename} not found.", silent=False)
        return
    except Exception as e:
        echo(f"An error occurred: {e}", silent=False)
        return
    # Example: remove_marker_and_patt(filename, output)
    echo("Done.", silent=False)


def main():
    cli()


if __name__ == "__main__":
    main()
