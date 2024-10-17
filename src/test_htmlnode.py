import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "b",
            "I am a test node",
            None,
            {"location": "home", "target": "blank"}
            )
        self.assertEqual(
            node.props_to_html(),
            ' location="home" target="blank"'
            )

    def test_values(self):
        node = HTMLNode(
            "b",
            "I am a test node"
        )
        
        self.assertEqual(
            node.tag,
            "b"
        )

        self.assertEqual(
            node.value,
            "I am a test node"
        )

        self.assertEqual(
            node.children,
            None
        )

        self.assertEqual(
            node.props,
            None
        )

    def test_repr(self):
        node = HTMLNode(
            "b",
            "I am a test node",
            None,
            {"location": "home"}
            )
        
        self.assertEqual(
            "HTMLNode(b, I am a test node, children: None, {'location': 'home'})",
            node.__repr__()
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "I am a test node")
        self.assertEqual(
            node.to_html(),
            "<p>I am a test node</p>"
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "I am a test node")
        self.assertEqual(
            node.to_html(),
            "I am a test node"
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("b", "I am a test child node")
        parent_node = ParentNode("p", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>I am a test child node</b></p>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("i", "I am a test grandchild node")
        child_node = ParentNode("b", [grandchild_node])
        parent_node = ParentNode("p", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b><i>I am a test grandchild node</i></b></p>"
        )

    def test_to_html_with_many_children(self):
        child_node = LeafNode("b", "I am a test child node")
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "I am a bold test node"),
                LeafNode("i", "I am an italic test node")
            ]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>I am a bold test node</b><i>I am an italic test node</i></p>"
        )
if __name__ == "__main__":
    unittest.main()