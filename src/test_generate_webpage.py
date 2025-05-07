import unittest
from generate_webpage import extract_title


class TestGenerateWebpage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Heading

This is not.


"""
        heading = extract_title(md)
        self.assertEqual(heading, "Heading")

    def test_missing_title(self):
        md = """
1. This is a list
2. And this too

This is not.


"""
        with self.assertRaises(ValueError, msg="Expected to find no heading"):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
