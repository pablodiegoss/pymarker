from PIL import Image

from .exceptions import BlackBorderSizeError, WhiteBorderSizeError
from .utils import (
    PattStr,
    add_border,
    calculate_border,
    check_path,
    color_to_file,
    create_and_open_patt,
    crop_black_borders,
    crop_white_borders,
    generate_white_background,
    get_dir,
    get_name,
    open_image,
    square_image,
)

DEFAULT_BLACK_BORDER_PERCENTAGE = 20
DEFAULT_WHITE_BORDER_PERCENTAGE = 3
DEFAULT_INNER_BORDER_PERCENTAGE = 0


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


def generate_marker_from_image(
    original_image: Image.Image,
    black_border_percentage=DEFAULT_BLACK_BORDER_PERCENTAGE,
    white_border_percentage=DEFAULT_WHITE_BORDER_PERCENTAGE,
    inner_border_percentage=DEFAULT_INNER_BORDER_PERCENTAGE,
) -> Image.Image:
    squared_image = square_image(original_image)

    # Create a white background if the image has transparency
    marker_middle_image = generate_white_background(squared_image)

    if inner_border_percentage != 0:
        try:
            inner_border_size = calculate_border(
                squared_image.height, (inner_border_percentage / 100)
            )
        except ValueError as e:
            raise WhiteBorderSizeError(str(e))
        # Add inner border
        white = (255, 255, 255)
        marker_middle_image = add_border(marker_middle_image, inner_border_size, white)

    try:
        black_border_size = calculate_border(
            squared_image.height, (black_border_percentage / 100)
        )
    except ValueError as e:
        raise BlackBorderSizeError(str(e))
    # Add black border
    black = (0, 0, 0)
    marker = add_border(marker_middle_image, black_border_size, black)

    if white_border_percentage != 0:
        try:
            white_border_size = calculate_border(
                squared_image.height, (white_border_percentage / 100)
            )
        except ValueError as e:
            raise WhiteBorderSizeError(str(e))

        # Add white border
        white = (255, 255, 255)
        marker = add_border(marker, white_border_size, white)

    return marker


def generate_marker(
    filename: str,
    black_border_percentage: int = DEFAULT_BLACK_BORDER_PERCENTAGE,
    output=None,
    white_border_percentage: int = DEFAULT_WHITE_BORDER_PERCENTAGE,
    inner_border_percentage=DEFAULT_INNER_BORDER_PERCENTAGE,
):
    if filename:
        image = open_image(filename)
        output = check_path(output) if output else get_dir(filename)
        name = get_name(filename)

        border_marker = generate_marker_from_image(
            image,
            black_border_percentage,
            white_border_percentage,
            inner_border_percentage,
        )

        border_marker.save(output + name + "_marker.png", "PNG")
    else:
        raise FileNotFoundError


def remove_borders(filename: str, output: str = None):
    """Remove white borders from marker images, cropping symmetrically until the black border."""
    if filename:
        image = open_image(filename)
        image = image.convert("RGB")

        # Crop White Borders
        cropped_image = crop_white_borders(image)
        # Crop Black Borders
        cropped_image = crop_black_borders(cropped_image)

        # Determine output path and filename
        if output:
            # If output ends with a slash, it's a directory
            if output.endswith("/") or output.endswith("\\"):
                name = get_name(filename)
                save_path = output + name + "_cropped.png"
            else:
                # If output looks like a filename (has .png or .jpg), use it directly
                if output.lower().endswith((".png", ".jpg", ".jpeg")):
                    save_path = output
                else:
                    # Otherwise, treat as directory
                    name = get_name(filename)
                    save_path = output + name + "_cropped.png"
        else:
            output = get_dir(filename)
            name = get_name(filename)
            save_path = output + name + "_cropped.png"

        cropped_image.save(save_path, "PNG")
    else:
        raise FileNotFoundError
