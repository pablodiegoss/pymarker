import unittest
from pymarker import generate_patt

class TestPattGenerator(unittest.TestCase):
    def test_output_patt(self):
        print(generate_patt())
        assert False