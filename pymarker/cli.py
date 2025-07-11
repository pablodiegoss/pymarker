import click
from .core import generate_marker, generate_patt
from .utils import echo


@click.command()
@click.argument("filename")
@click.option("--patt", "-p", is_flag=True, default=False)
@click.option("--marker", "-m", is_flag=True, default=False)
@click.option("--string", "-s", is_flag=True, default=False)
@click.option("--black-border-size", "-b", default=50)  # 50% is based on template hiro marker
@click.option("--white-border-size", "-w", default=3)
@click.option("--output", "-o", default=None, type=str)
def generate_patt_and_marker(filename, patt, marker, string, black_border_size, white_border_size, output):
    echo("-- Starting PyMarker Generator --".format(), silent=string)
    if (patt and marker) or (not patt and not marker):
        echo("Generating patt and marker for {}".format(filename), silent=string)
        # generate_patt must be silent if you are not using the flag string.
        echo(generate_patt(filename, output, string), silent=not string)
        generate_marker(filename, black_border_size, output, white_border_size)
    elif marker:
        echo("Generating marker for {}".format(filename), silent=string)
        generate_marker(filename, black_border_size, output, white_border_size)
    elif patt:
        echo("Generating patt for {}".format(filename), silent=string)
        echo(generate_patt(filename, output, string), silent=not string)

    echo("Done.", silent=string)


def main():
    generate_patt_and_marker()


if __name__ == "__main__":
    main()
