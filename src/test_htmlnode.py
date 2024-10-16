import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "This is an HTML node")
        node2 = HTMLNode("p", "This is an HTML node")
        self.assertEqual(node, node2)

    def test_noeq_tag(self):
        node = HTMLNode("p", "This is an HTML node", props = {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("h1", "This is an HTML node", props = {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node, node2)

    def test_noeq_value(self):
        node = HTMLNode("p", "This is an HTML node", props = {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("p", "This is also an HTML node", props = {"href": "https://www.google.com", "target": "_blank",})
        self.assertNotEqual(node, node2)

    def test_noeq_children(self):
        pass

    def test_noeq_props(self):
        node = HTMLNode("p", "This is an HTML node", props = {"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode("p", "This is an HTML node", props = {"href": "https://www.google.com",})
        self.assertNotEqual(node, node2)

    def test_prop_to_html(self):
        node = HTMLNode("p", "This is an HTML node", props = {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()