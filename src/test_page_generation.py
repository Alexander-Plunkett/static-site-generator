import unittest

from page_generation import extract_title

class TestExtractHeading(unittest.TestCase):
    def test_single_heading(self):
        markdown = """
# I am a heading...         
"""

        self.assertEqual(
            extract_title(markdown),
            "I am a heading..."
        )
    
    def test_disguised_heading(self):
        markdown = """
* I'm
* A
* List

# I am a heading...         
"""

        self.assertEqual(
            extract_title(markdown),
            "I am a heading..."
        )