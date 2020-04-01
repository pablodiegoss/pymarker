import unittest
from pymarker import generate_png

class TestPngGenerator(unittest.TestCase):
    def test_output_png(self):
        print(generate_png())
        assert False
