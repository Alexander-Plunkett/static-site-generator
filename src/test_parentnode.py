import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_no_tag(self):
        node = ParentNode(children = [LeafNode("b", "Bold text")])
        self.assertRaises(ValueError)

    def test_no_children(self):
        node = ParentNode("p")
        self.assertRaises(ValueError)

    def test_nested_parentnodes(self):
        node = ParentNode("p", [ParentNode("b", [LeafNode("i", "Italic text")])])
        self.assertEqual(node.to_html(), '<p><b><i>Italic text</i></b></p>')

    def test_multiple_children(self):
        node = ParentNode("p", [LeafNode("i", "Italic text"), LeafNode(value = "Normal text")])
        self.assertEqual(node.to_html(), '<p><i>Italic text</i>Normal text</p>')

    def test_nested_and_leaf_children(self):
        node = ParentNode("p", [ParentNode("b", [LeafNode("i", "Italic text")]), LeafNode(value = "Normal text")])
        self.assertEqual(node.to_html(), '<p><b><i>Italic text</i></b>Normal text</p>')