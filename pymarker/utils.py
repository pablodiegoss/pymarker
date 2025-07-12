import os
from math import ceil

import click
from PIL import Image


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


def square_image(image: Image.Image) -> Image.Image:
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


def get_marker_size(image: int, border_size: int) -> tuple:
    size = image.height + (border_size * 2)
    # Using the size double because the resulting marker should be a square.
    return (size, size)


def create_empty_patt(filename):
    patt_name = remove_extension(filename) + ".patt"
    patt_file = open(patt_name, "w")
    patt_file.close()
    return patt_name


def create_and_open_patt(filename):
    patt_name = create_empty_patt(filename)
    return open(patt_name, "a")


def patt_number_format(point):
    return str(point).rjust(3, " ")


def find_margin_size(image: Image.Image, colors: [tuple]) -> int:
    # Find how many pixels of "colors" border are present by scanning horizontally from the vertical center row
    pixels = image.load()
    center_y = image.height // 2
    margin = None
    for x in range(image.width // 2):
        if pixels[x, center_y] not in colors:
            margin = x
            break

    return margin


def crop_white_borders(image: Image.Image) -> Image.Image:
    # All shades of white or grey that are found in marker borders
    colors = [
        (255, 255, 255),
        (254, 254, 254),
        (251, 251, 251),
        (250, 250, 250),
        (252, 252, 252),
        (253, 253, 253),
        (249, 249, 249),
        (248, 248, 248),
        (247, 247, 247),
        (246, 246, 246),
        (253, 253, 253),
        (51, 51, 51),
        (54, 54, 54),
        (151, 151, 151),
    ]
    white_margin = find_margin_size(image, colors)
    if white_margin is not None:
        return image.crop(
            (
                white_margin,
                white_margin,
                image.width - white_margin,
                image.height - white_margin,
            )
        )
    return image


def crop_black_borders(image: Image.Image) -> Image.Image:
    # All shades of black or grey that are found in marker borders
    colors = [
        (0, 0, 0),
        (1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 4),
        (5, 5, 5),
        (6, 6, 6),
        (7, 7, 7),
        (13, 12, 14),
        (13, 13, 13),
        (0, 0, 1),
        (51, 51, 51),
        (52, 52, 52),
        (14, 14, 14),
        (50, 50, 50),
        (48, 48, 48),
        (67, 67, 67),
    ]
    black_margin = find_margin_size(image, colors)
    if black_margin is not None:
        if black_margin > image.width * 0.3:  # Avoid cropping too much on markers
            black_margin = int(image.width * 0.2)
        return image.crop(
            (
                black_margin,
                black_margin,
                image.width - black_margin,
                image.height - black_margin,
            )
        )
    return image


# Prints all pixels from a split color to the patt file
def color_to_file(c, patt):
    n = 1
    for point in list(c.getdata()):
        patt.write(patt_number_format(point))
        if n != 0 and n % 16 == 0:
            n = 0
            patt.write("\n")
        else:
            patt.write(" ")
        n += 1


def add_border(image: Image.Image, border_size: int, color: tuple) -> Image.Image:
    image_border_size: tuple = get_marker_size(image, border_size)
    border_marker = Image.new("RGB", image_border_size, color)
    border_marker.paste(image, get_box_coords(image, border_size))

    return border_marker


def calculate_border(image_size: float, border_ratio: float = 0.2) -> float:
    """
    Calculates the border thickness (Y) so that each border represents
    a proportion of the total size of the image with border.

    Parameters:
    - image_size (float): original size of the image (width or height).
    - border_ratio (float): desired border ratio relative to the final size (e.g., 0.2 for 20%).

    Returns:
    - int: border size in pixels.
    """
    if not (0 < border_ratio < 0.5):
        raise ValueError("The border ratio must be between 0 and 0.5 (exclusive)")

    y = (border_ratio * image_size) / (1 - 2 * border_ratio)
    return ceil(y)


# Ensure the image has a white background, not transparent
def generate_white_background(image: Image.Image) -> Image.Image:
    # If the image has an alpha channel, create a white background
    if len(image.split()) > 3:
        # Create a new image with filled with white
        white_image = Image.new("RGB", image.size, (255, 255, 255))
        # Paste the original image onto the white background using its alpha channel as a mask
        white_image.paste(image, mask=image.split()[3])
        return white_image
    return image


class PattStr:
    def __init__(self):
        self.content = ""

    def __repr__(self):
        return self.content.rstrip() + "\n"

    def write(self, data):
        self.content += data

    def close(self):
        return str(self)
