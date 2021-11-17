import unittest
import triangle_area


class TetsArea(unittest.TestCase):

    # runTest function will be execute even if it doesn't start with 'test' string.
    def runTest(self):
        result = triangle_area.triangle(10, 5)
        self.assertEqual(result, 25)

if __name__ == '__main__':
    unittest.main()