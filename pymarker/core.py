from .utils import (
    open_image,
    get_box_coords,
    remove_extension,
    get_dir,
    get_name,
    check_path,
    PattStr,
)
from PIL import Image
from math import ceil


def get_marker_size(image, border_size):
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


def generate_patt(filename, output=None, string=False):
    if filename:
        image = open_image(filename)
        # Patt default marker size is 16x16 pixels
        image = image.resize((16, 16))

        output = check_path(output) if output else get_dir(filename)
        name = get_name(filename)

        patt = PattStr() if string else create_and_open_patt(output + name)
        for i in range(0, 4):
            r, g, b = image.split()
            color_to_file(r, patt)
            color_to_file(g, patt)
            color_to_file(b, patt)
            if(i != 3):
                patt.write("\n")
            image = image.rotate(90)

        return patt.close()
    else:
        raise FileNotFoundError

def patt_number_format(point):
    return str(point).rjust(3, " ")


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


def generate_marker(filename, border_percentage=50, output=None):
    if filename:
        image = open_image(filename)
        output = check_path(output) if output else get_dir(filename)
        name = get_name(filename)

        border_size = ceil(image.height * (border_percentage / 100))

        # Default color is black, setting (0, 0, 0) for clarity, as the border should be black
        marker_size = get_marker_size(image, border_size)
        marker = Image.new("RGB", marker_size, (0, 0, 0))
        marker.paste(image, get_box_coords(image, border_size))
        marker.save(output + name + "_marker.png", "PNG")
    else:
        raise FileNotFoundError