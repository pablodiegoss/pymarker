import unittest
from pymarker import generate_marker
from pymarker.exceptions import BlackBorderSizeError, WhiteBorderSizeError
import filecmp as fc
import os

KEEP_FILES = False  # Set to True to keep generated files after tests
class TestMarkerGenerator(unittest.TestCase):
    def test_output_marker(self):
        """Test that marker is generated and matches the expected output."""
        input_image = "tests/input/hiro.jpg"
        output_file = "tests/input/hiro_marker.png"
        generate_marker(input_image)
        try:
            self.assertTrue(fc.cmp(output_file, "tests/output/hiro_marker_b20_w3.png"))
        finally:
            if os.path.exists(output_file) and not KEEP_FILES:
                os.remove(output_file)

    def test_no_input(self):
        """Testing that no input raises an error for generating markers"""
        border_size = 20
        try:
            generate_marker(None, border_size, None)
        except FileNotFoundError:
            assert True

    def test_output_folder(self):
        """Tests if the user is able to use the -o flag
        which defines an output folder for his marker"""

        input_image = "tests/input/hiro.jpg"
        output_folder = "tests/automated/"
        generate_marker(filename=input_image, output=output_folder)
        f = open(output_folder + "hiro_marker.png", "r")
        if f:
            f.close()
            if not KEEP_FILES:
                os.remove(output_folder + "hiro_marker.png")
            assert True
        else:
            assert False

    def test_black_border_size(self):
        """Tests if the user can define a border size using -b
        checking for border_size 20% which is default and 10%.
        """
        input_image = "tests/input/hiro.jpg"
        border_size = 10
        output_folder = "tests/automated/"

        generate_marker(input_image, border_size, output_folder)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b10_w3.png"
        )
        if not KEEP_FILES:
            os.remove(output_folder + "hiro_marker.png")

        border_size = 20
        generate_marker(input_image, border_size, output_folder)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b20_w3.png"
        )
        if not KEEP_FILES:
                os.remove(output_folder + "hiro_marker.png")
    
    def test_white_border_size(self):
        """Tests if the user can define a white border size using -w
        checking for border_size 3% which is default and 0% as not having a white border.
        """
        input_image = "tests/input/hiro.jpg"
        border_size = 0
        output_folder = "tests/automated/"

        generate_marker(input_image, 20, output_folder, border_size)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b20_w0.png"
        )
        if not KEEP_FILES:
                os.remove(output_folder + "hiro_marker.png")

        border_size = 20
        generate_marker(input_image, 20, output_folder, border_size)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b20_w20.png"
        )
        if not KEEP_FILES:
                os.remove(output_folder + "hiro_marker.png")


    def test_invalid_border_sizes(self):
        """Tests if the user can define a border size using -b
        checking for border_size 0% and 50% which are invalid.
        """
        input_image = "tests/input/hiro.jpg"
        output_folder = "tests/automated/"

        # Testing black border size
        with self.assertRaises(BlackBorderSizeError):
            generate_marker(input_image, 0, output_folder)

        with self.assertRaises(BlackBorderSizeError):
            generate_marker(input_image, 50, output_folder)

        # Testing white border size
        with self.assertRaises(WhiteBorderSizeError):
            generate_marker(input_image, 20, output_folder, -1)

        with self.assertRaises(WhiteBorderSizeError):
            generate_marker(input_image, 20, output_folder, 50)
        
        with self.assertRaises(WhiteBorderSizeError):
            generate_marker(input_image, 20, output_folder, 3, -1)
        
        with self.assertRaises(WhiteBorderSizeError):
            generate_marker(input_image, 20, output_folder, 3, 50)
    
    def test_inner_border_size(self):
        """Tests if the user can define an inner border size using -i
        checking for inner_border_size 3% which is default and 0% as not having an inner border.
        """
        input_image = "tests/input/hiro.jpg"
        output_folder = "tests/automated/"

        generate_marker(input_image, 20, output_folder, 3)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b20_w3.png"
        )
        if not KEEP_FILES:
                os.remove(output_folder + "hiro_marker.png")

        generate_marker(input_image, 20, output_folder, 3, 2)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b20_w3_i2.png"
        )
        if not KEEP_FILES:
                os.remove(output_folder + "hiro_marker.png")