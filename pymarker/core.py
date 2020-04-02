from utils import open_image, get_box_coords, remove_extension
from PIL import Image

def get_marker_size(image, border_size):
    # There are two borders (left and right) and (up and down)
    size = image.height + (border_size*2)
    # Using the height double because the resulting marker should be a square.
    return (size,size)

def generate_patt(filename):
    return "000"

def generate_png(filename, border_size):
    image = open_image(filename)
    # Default color is black, setting (0, 0, 0) for clarity, as the border should be black
    marker_size = get_marker_size(image, border_size)
    marker = Image.new('RGB', marker_size, (0, 0, 0))
    marker.paste(image,get_box_coords(image,border_size))
    marker.save(remove_extension(filename)+".png", "PNG")
    return True
