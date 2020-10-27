import os
from PIL import Image
import click


def get_current_dir():
    # Slash added at the end to append with filenames
    return os.path.abspath(".") + "/"


def open_image(filename):
    image_path = get_current_dir() + filename
    try:
        image = Image.open(image_path)
    except IOError:
        raise FileNotFoundError

    return square_image(image)


def square_image(image):
    limited_size = image.width if image.height > image.width else image.height
    return image.resize((limited_size, limited_size))


# Coords used when pasting the original image inside the black canvas to create borders
def get_box_coords(image, border_size):
    # left, upper, right, lower bounds in pixels
    return (
        border_size,
        border_size,
        border_size + image.width,
        border_size + image.height,
    )


# The filename contains extension and/or folders that should be filtered
def remove_extension(filename):
    return filename.split(".")[0]


# Get folder location of file
def get_dir(filename):
    # Avoid error on paths without '/' at the end
    folder = filename if filename[-1] == "/" else filename + "/"
    return folder.rsplit("/", 2)[0] + "/"


# Get name of the file from a filepath
def get_name(filename):
    name = filename.rsplit("/", 1)[1]
    return name.split(".")[0]


# Check and return folder path with '/' if necessary
def check_path(path):
    path = path if path[-1] == "/" else path + "/"
    return path


def echo(string, silent=False, *params, **kwargs):
    if not silent:
        click.echo(string, *params, **kwargs)


class PattStr:
    def __init__(self):
        self.content = ""

    def __repr__(self):
        return self.content.rstrip() + "\n"

    def write(self, data):
        self.content += data

    def close(self):
        return str(self)
