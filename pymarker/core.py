from .utils import (
    open_image,
    get_box_coords,
    remove_extension,
    get_dir,
    get_name,
    check_path,
    PattStr,
    square_image,
    get_marker_size,
    create_and_open_patt,
    create_empty_patt,
    color_to_file,
    patt_number_format,
    calculate_border,
)
from PIL import Image


def generate_patt(filename: str, output: str = None, string: bool = False):
    if filename:
        image = open_image(filename)
        # Patt default marker size is 16x16 pixels
        image = image.resize((16, 16))

        output = check_path(output) if output else get_dir(filename)
        name = get_name(filename)

        new_image = generate_white_background(image)

        patt = PattStr() if string else create_and_open_patt(output + name)
        for i in range(0, 4):
            r, g, b = new_image.split()
            color_to_file(r, patt)
            color_to_file(g, patt)
            color_to_file(b, patt)
            if i != 3:
                patt.write("\n")
            new_image = new_image.rotate(90)

        return patt.close()
    else:
        raise FileNotFoundError


def generate_patt_from_image(image: Image.Image) -> PattStr:

    # Patt default marker size is 16x16 pixels
    image = image.resize((16, 16))

    new_image = generate_white_background(image)

    patt = PattStr()
    for i in range(0, 4):
        r, g, b = new_image.split()
        color_to_file(r, patt)
        color_to_file(g, patt)
        color_to_file(b, patt)
        if i != 3:
            patt.write("\n")
        new_image = new_image.rotate(90)

    return patt.close()

def add_border(image: Image.Image, border_size: int, color: tuple) -> Image.Image:
    image_and_black_border_size:tuple = get_marker_size(image, border_size)
    black_border_marker = Image.new("RGB", image_and_black_border_size, color)
    black_border_marker.paste(image, get_box_coords(image, border_size))

    return black_border_marker



def generate_marker_from_image(original_image: Image.Image, black_border_percentage=50, white_border_percentage=3) -> Image.Image:

    squared_image = square_image(original_image)
    
    black_border_size = calculate_border(squared_image.height, (black_border_percentage / 100))
    white_border_size = calculate_border(squared_image.height, (white_border_percentage / 100))

    # Create a white background if the image has transparency
    marker_middle_image = generate_white_background(squared_image)

    # Add black border
    black = (0, 0, 0)
    black_border_marker = add_border(marker_middle_image, black_border_size, black)

    # Add white border
    white = (255, 255, 255)
    white_border_marker = add_border(black_border_marker, white_border_size, white)

    return white_border_marker





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


def generate_marker(filename:str, black_border_percentage:int=50,output=None, white_border_percentage:int=3):
    if filename:
        image = open_image(filename)
        output = check_path(output) if output else get_dir(filename)
        name = get_name(filename)

        black_border_size = calculate_border(image.height, (black_border_percentage / 100))
        white_border_size = calculate_border(image.height, (white_border_percentage / 100))

        new_image = generate_white_background(image)

        # Default color is black, setting (0, 0, 0) for clarity, as the border should be black
        black_border_marker = add_border(new_image, black_border_size, (0, 0, 0))
        white_border_marker = add_border(black_border_marker, white_border_size, (255, 255, 255))
        white_border_marker.save(output + name + "_marker.png", "PNG")
    else:
        raise FileNotFoundError
