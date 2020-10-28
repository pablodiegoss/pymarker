import unittest
from pymarker import generate_patt
import filecmp as fc
import os


class TestPattGenerator(unittest.TestCase):
    def test_output_patt(self):
        """Testing that pattern file is being generated"""
        input_image = "tests/input/hiro.jpg"
        generate_patt(input_image)
        f = open("tests/input/hiro.patt", "r")
        if f:
            try:
                assert fc.cmp("tests/input/hiro.patt", "tests/output/hiro.patt")
            except:
                assert False
            finally:
                f.close()
                os.remove("tests/input/hiro.patt")
            assert True
        else:
            assert False

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
        f = open("tests/output/hiro.patt", "r")
        try:
            assert patt_str == f.read()
        except:
            assert False
        finally:
            f.close()
