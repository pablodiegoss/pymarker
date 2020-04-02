import os 
from PIL import Image

def get_current_dir():
    # Slash added at the end to append with filenames
    return os.path.abspath('.') + '/'

def open_image(filename):
    image_path = get_current_dir() + filename    
    try:
        image = Image.open(image_path)
    except IOError:
        raise FileNotFoundError
    
    return square_image(image)

def square_image(image):
    limited_size = image.width if image.height>image.width else image.height
    return image.resize((limited_size,limited_size))
    
# Coords used when pasting the original image inside the black canvas to create borders
def get_box_coords(image, border_size):
    # left, upper, right, lower bounds in pixels
    return (border_size,
            border_size, 
            border_size + image.width,
            border_size + image.height
            )


# The filename contains extension and/or folders that should be filtered
def remove_extension(filename):
    return filename.split(".")[0]