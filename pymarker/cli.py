import click
from core import generate_png, generate_patt

@click.command()
@click.argument('filename')
@click.option('--patt','-p', is_flag=True, default=False)
@click.option('--marker','-m', is_flag=True, default=False)
def generate_patt_and_png(filename, patt, marker):
    click.echo("-- Starting PyMarker Generator --".format(filename))

    if (patt and marker) or (not patt and not marker):
        generate_patt(filename)
        generate_png(filename)
        click.echo("Generating patt and marker for {}".format(filename))
    elif marker:
        generate_png(filename)
        click.echo("Generating marker for {}".format(filename))
    elif patt:
        generate_patt(filename)
        click.echo("Generating patt for {}".format(filename))

    click.echo("Done.")

if __name__ == "__main__":
    generate_patt_and_png()