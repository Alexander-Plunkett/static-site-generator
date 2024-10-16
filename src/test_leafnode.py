import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_tag(self):
        node = LeafNode(value = "This is a leaf node", props = {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.to_html(), "This is a leaf node")

    def test_no_props(self):
        node = LeafNode("b", "This is a leaf node")
        self.assertEqual(node.to_html(), "<b>This is a leaf node</b>")

    def test_no_props(self):
        node = LeafNode("a", "This is a leaf node", props = {"href": "https://www.google.com",})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">This is a leaf node</a>')

    def test_no_value(self):
        node = LeafNode("b")
        self.assertRaises(ValueError)

if __name__ == "__main__":
    unittest.main()