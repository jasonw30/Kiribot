import unittest

class AnAbsolutelyUselessException(Exception):

    def __doc__(self):
        return "A useless exception"
    

def uselessfunction(*args):
    raise AnAbsolutelyUselessException("Apparently it works?")

class unittestmain(unittest.TestCase):

    def test_main(self):
        self.assertRaises(AnAbsolutelyUselessException, uselessfunction, ">.<")


if __name__ == "__main__":
    unittest.main()