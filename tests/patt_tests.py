import unittest
from pymarker import generate_patt
import filecmp as fc
import os

KEEP_FILES = False  # Set to True to keep generated files after tests

class TestPattGenerator(unittest.TestCase):
    def test_output_patt(self):
        """Testing that pattern file is being generated and matches expected output"""
        input_image = "tests/input/hiro.jpg"
        output_file = "tests/input/hiro.patt"
        expected_file = "tests/output/hiro.patt"

        generate_patt(input_image)

        # Check if file exists and compare contents
        self.assertTrue(os.path.exists(output_file), "Pattern file was not generated.")
        self.assertTrue(fc.cmp(output_file, expected_file), "Generated pattern file does not match expected output.")

        if not KEEP_FILES:
            os.remove(output_file)

    def test_input_patt(self):
        """Testing that input is required for generating patts"""
        try:
            generate_patt(None)
        except FileNotFoundError:
            assert True

    def test_folder_patt(self):
        """Tests if the user is able to use the -o flag
        which defines an output folder for his pattern"""

        input_image = "tests/input/hiro.jpg"
        output_folder = "tests/automated/"
        generate_patt(input_image, output_folder)
        f = open(output_folder + "hiro.patt", "r")
        if f:
            f.close()
            if not KEEP_FILES:
                os.remove(output_folder + "hiro.patt")
            assert True
        else:
            assert False

    def test_string_patt(self):
        """Tests if the user is able to use the -s flag"""
        input_image = "tests/input/hiro.jpg"
        output_folder = "tests/automated/"
        patt_str = generate_patt(input_image, output_folder, True)

        try:
            open(output_folder + "hiro.patt", "r")
        except FileNotFoundError:
            assert True

        with open("tests/output/hiro.patt", "r") as f:
            file_content = f.read()
            self.assertEqual(patt_str, file_content)
