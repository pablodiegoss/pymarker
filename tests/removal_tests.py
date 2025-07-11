import unittest
from pymarker import remove_borders

import os
from PIL import Image, ImageChops

KEEP_FILES = False  # Set to True to keep generated files after tests
class TestBorderRemover(unittest.TestCase):

    def test_remove_with_white_borders(self):
        input_image = "tests/input/hiro_bw.png"
        output_image = "tests/automated/hiro_cropped.png"
        remove_borders(input_image, output=output_image)
        self.assertTrue(os.path.exists(output_image))
        img1 = Image.open(output_image)
        img2 = Image.open("tests/output/hiro_cropped.png")
        diff = ImageChops.difference(img1, img2)
        # Allow a small tolerance for minor differences
        bbox = diff.getbbox()
        self.assertTrue(bbox is None or diff.getextrema()[0][1] < 5)
        if not KEEP_FILES:
            os.remove(output_image)

    def test_remove_with_black_borders(self):
        input_image = "tests/input/hiro_b.png"
        output_image = "tests/automated/hiro_b_cropped.png"
        remove_borders(input_image, output=output_image)
        self.assertTrue(os.path.exists(output_image))
        img1 = Image.open(output_image)
        img2 = Image.open("tests/output/hiro_cropped.png")
        diff = ImageChops.difference(img1, img2)
        # Allow a small tolerance for minor differences
        bbox = diff.getbbox()
        self.assertTrue(bbox is None or diff.getextrema()[0][1] < 5)
        if not KEEP_FILES:
            os.remove(output_image)