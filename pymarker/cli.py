import click
from .core import generate_marker, generate_patt

@click.command()
@click.argument('filename')
@click.option('--patt','-p', is_flag=True, default=False)
@click.option('--marker','-m', is_flag=True, default=False)
@click.option('--string','-s', is_flag=True, default=False)
@click.option('--border-size', '-b', default=50) # 50% is based on template hiro marker
@click.option('--output','-o', default=None, type=str)
def generate_patt_and_marker(filename, patt, marker, string, border_size, output):
    click.echo("-- Starting PyMarker Generator --".format(filename))
    if (patt and marker) or (not patt and not marker):
        click.echo("Generating patt and marker for {}".format(filename))
        generate_patt(filename, output, string)
        generate_marker(filename, border_size, output)
    elif marker:
        click.echo("Generating marker for {}".format(filename))
        generate_marker(filename, border_size, output)
    elif patt:
        click.echo("Generating patt for {}".format(filename))
        generate_patt(filename, output, string)

    click.echo("Done.")

def main():
    generate_patt_and_marker()

if __name__ == "__main__":
    main()
