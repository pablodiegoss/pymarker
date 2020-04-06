import unittest
from pymarker import generate_marker

class TestMarkerGenerator(unittest.TestCase):
    def test_output_marker(self):
        print(generate_marker())
        assert False
