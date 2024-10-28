import unittest

from htmlnode import LeafNode, ParentNode

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    heading_counter,
    markdown_to_html_node,
    BlockType)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading", 
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
# This is another heading




This is just a paragraph of text.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is another heading", 
                "This is just a paragraph of text.",
            ]
        )

    def test_headings(self):
        block = ("### This is a h3 heading")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.HEADING
        )

    def test_code(self):
        block = ("```\nThis is a code block\n```")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_quote(self):
        block = (">This is a quote\n>This is another quote")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_unordered_list(self):
        block = ("- This is an unordered list item\n- This is another unordered list item")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ULIST
        )

    def test_unordered_list_alt(self):
        block = ("* This is an unordered list item\n* This is another unordered list item")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ULIST
        )

    def test_ordered_list(self):
        block = ("1. This is an ordered list item\n2. This is another ordered list item\n3. This is the 3rd ordered list item")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.OLIST
        )

    def test_paragraph(self):
        block = ("I am a paragraph")
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

class TestBlockToHTML(unittest.TestCase):
    def test_heading_counter(self):
        block = ("###### This is a heading")
        self.assertEqual(
            heading_counter(block),
            "h6"
        )

    def full_test(self):
        file = open("test_file.md", "r")
        markdown = file.read()
        return_node = markdown_to_html_node(markdown)
        expected_node = ParentNode("div", children = [
                            ParentNode("h1", children = [LeafNode(None, "Test Start")]),
                            ParentNode("p", children = [
                                LeafNode(None, "Welcome to the "), 
                                LeafNode("b", "start"),
                                LeafNode(None, " of the test")]),
                            ParentNode("blockquote", children = [
                                LeafNode(None, "I "), 
                                LeafNode("i", "hope"),
                                LeafNode(None, " this works")]),
                            ParentNode("pre", children = [LeafNode("code", "This is a code block")]),
                            ParentNode("h3", children = [LeafNode(None, "Image list")]),
                            ParentNode("ol", children = [
                                ParentNode("li", children = [
                                    LeafNode(None, "This is the first image"), 
                                    LeafNode("img", None, {"src": "https://imgur.com/kJ9BLCa", "alt": "clarkson"})]),
                                ParentNode("li", children = [
                                    LeafNode(None, "This is the second image"), 
                                    LeafNode("img", None, {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan"})])]),
                            ParentNode("h4", children = [LeafNode(None, "Link list")]),
                            ParentNode("ul", children = [
                                ParentNode("li", children = [
                                    LeafNode("a", "Link", {"href": "https://www.boot.dev"}),
                                    LeafNode(None, " to boot dev")]),
                                ParentNode("li", children = [
                                    LeafNode("a", "Link", {"href": "https://github.com/Alexander-Plunkett"}),
                                    LeafNode(None, " to my github")])]),
                            ParentNode("p", children = [LeafNode(None, "That ends the test")])])
        file.close()
        self.assertEqual(
            return_node,
            expected_node
        )

if __name__ == "__main__":
    unittest.main()