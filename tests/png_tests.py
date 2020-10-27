import unittest
from pymarker import generate_marker
import filecmp as fc
import os


class TestMarkerGenerator(unittest.TestCase):
    def test_output_marker(self):
        """Testing that marker is being generated"""
        input_image = "tests/input/hiro.jpg"
        generate_marker(input_image)
        f = open("tests/input/hiro_marker.png", "r")
        if f:
            try:
                assert fc.cmp(
                    "tests/input/hiro_marker.png", "tests/output/hiro_marker_b50.png"
                )
            except:
                assert False
            finally:
                f.close()
                os.remove("tests/input/hiro_marker.png")
            assert True
        else:
            assert False

    def test_no_input(self):
        """Testing that no input raises an error for generating markers"""
        border_size = 50
        try:
            generate_marker(None, border_size, None)
        except FileNotFoundError:
            assert True

    def test_output_folder(self):
        """Tests if the user is able to use the -o flag
        which defines an output folder for his marker"""

        input_image = "tests/input/hiro.jpg"
        border_size = 50
        output_folder = "tests/automated/"
        generate_marker(input_image, border_size, output_folder)
        f = open(output_folder + "hiro_marker.png", "r")
        if f:
            f.close()
            os.remove(output_folder + "hiro_marker.png")
            assert True
        else:
            assert False

    def test_border_size(self):
        """Tests if the user can define a border size using -b
        checking for border_size 50% which is default and 25%.
        """
        input_image = "tests/input/hiro.jpg"
        border_size = 25
        output_folder = "tests/automated/"
        generate_marker(input_image, border_size, output_folder)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b25.png"
        )

        border_size = 50
        generate_marker(input_image, border_size, output_folder)
        assert fc.cmp(
            output_folder + "hiro_marker.png", "tests/output/hiro_marker_b50.png"
        )
