from utils import open_image, get_box_coords, remove_extension
from PIL import Image

def get_marker_size(image, border_size):
    # There are two borders (left and right) and (up and down)
    size = image.height + (border_size*2)
    # Using the height double because the resulting marker should be a square.
    return (size,size)

def create_empty_patt(filename):
    patt_name = remove_extension(filename)+".patt"
    patt_file = open(patt_name, "w")
    patt_file.close()
    return patt_name

def generate_patt(filename):
    image = open_image(filename)
    # Patt default marker size is 16x16 pixels
    image = image.resize((16,16))
    
    patt_name = create_empty_patt(filename)
    patt = open(patt_name,"a")
    for _ in range(0,4):
        r, g, b = image.split()
        color_to_file(r, patt)
        color_to_file(g, patt)
        color_to_file(b, patt)
        patt.write('\n')
        image = image.rotate(90)

    patt.close()
    return True

def patt_number_format(point):
    return str(point).rjust(3,' ')    

# Prints all pixels from a split color to the patt file
def color_to_file(c, patt):
        n = 1
        for point in list(c.getdata()):
            patt.write(patt_number_format(point))
            if(n != 0 and n % 16 == 0):
                n = 0
                patt.write('\n')
            else:
                patt.write(' ')
            n += 1
        
def generate_png(filename, border_size):
    image = open_image(filename)
    # Default color is black, setting (0, 0, 0) for clarity, as the border should be black
    marker_size = get_marker_size(image, border_size)
    marker = Image.new('RGB', marker_size, (0, 0, 0))
    marker.paste(image,get_box_coords(image,border_size))
    marker.save(remove_extension(filename)+"_marker.png", "PNG")
    return True
