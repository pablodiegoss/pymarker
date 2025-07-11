import click

from .core import generate_marker, generate_patt
from .exceptions import BlackBorderSizeError, WhiteBorderSizeError
from .utils import echo


@click.command()
@click.argument("filename")
@click.option("--patt", "-p", is_flag=True, default=False)
@click.option("--marker", "-m", is_flag=True, default=False)
@click.option("--as_string", "-s", is_flag=True, default=False)
@click.option("--black-border-size", "-b", default=20)
@click.option("--white-border-size", "-w", default=3)
@click.option("--output", "-o", default=None, type=str)
def generate_patt_and_marker(
    filename, patt, marker, as_string, black_border_size, white_border_size, output
):
    echo("-- Starting PyMarker Generator --".format(), silent=as_string)
    if marker or (not patt and not marker):
        echo("Generating marker for {}".format(filename), silent=as_string)
        try:
            generate_marker(filename, black_border_size, output, white_border_size)
        except BlackBorderSizeError:
            echo("Black border size cannot be less or equal 0 or bigger than 50%")
            return
        except WhiteBorderSizeError:
            echo("White border size cannot be less than 0 or bigger than 50%")
            return

    if patt or (not patt and not marker):
        echo("Generating patt for {}".format(filename), silent=as_string)
        echo(generate_patt(filename, output, as_string), silent=not as_string)

    echo("Done.", silent=as_string)


def main():
    generate_patt_and_marker()


if __name__ == "__main__":
    main()
