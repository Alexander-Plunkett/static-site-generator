import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnode)

from textnode import TextNode, TextType

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_split(self):
        node = TextNode("I am a text node with **bold** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("I am a text node with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT)
            ]
        )

    def test_end_italic_split(self):
        node = TextNode("I am a text node with *italic text*", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "*", TextType.ITALIC),
            [
                TextNode("I am a text node with ", TextType.TEXT),
                TextNode("italic text", TextType.ITALIC)
            ]
        )

    def test_multiple_code_split(self):
        node = TextNode("I am a text node with `not one` but `two code blocks`", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("I am a text node with ", TextType.TEXT),
                TextNode("not one", TextType.CODE),
                TextNode(" but ", TextType.TEXT),
                TextNode("two code blocks", TextType.CODE)
            ]
        )

    def test_multiple_formats(self):
        node = TextNode("I am a text node with both **bold** and *italic* blocks", TextType.TEXT)
        partial_split = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            split_nodes_delimiter(partial_split, "*", TextType.ITALIC),
            [
                TextNode("I am a text node with both ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" blocks", TextType.TEXT)

            ]
        )

class TestImageAndLinkExtraction(unittest.TestCase):
    def test_image_extraction(self):
        text = "I am a text node with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        )

    def test_link_extraction(self):
        text = "I am a text node with a link [to boot dev](https://www.boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev")]
        )

    def test_multiple_link_extraction(self):
        text = "I am a text node with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_link_and_image_extraction(self):
        text = "I am a text node with a link [to google](https://www.google.co.uk) and a ![pingu](https://imgur.com/gallery/noot-noot-pingu-dyTMsQV)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to google", "https://www.google.co.uk")]
        )
        
        self.assertEqual(
            extract_markdown_images(text),
            [("pingu", "https://imgur.com/gallery/noot-noot-pingu-dyTMsQV")]
        )

class TestSplitNodes(unittest.TestCase):
    def test_image_split(self):
        node = TextNode("I am a text node with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("I am a text node with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")
            ]
        )

    def test_link_split(self):
        node = TextNode("I am a text node with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("I am a text node with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ]
        )

    def test_multiple_link_split(self):
        node = TextNode("I am a text node with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) as well", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("I am a text node with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" as well", TextType.TEXT)
            ]
        )

    def test_image_and_link_split(self):
        node = TextNode("I am a text node with both a ![clarkson gif](https://imgur.com/kJ9BLCa) and a link [to my github](https://github.com/Alexander-Plunkett) too", TextType.TEXT)
        partial_split = split_nodes_image([node])
        self.assertEqual(
            split_nodes_link(partial_split),
            [
                TextNode("I am a text node with both a ", TextType.TEXT),
                TextNode("clarkson gif", TextType.IMAGE, "https://imgur.com/kJ9BLCa"),
                TextNode(" and a link ", TextType.TEXT),
                TextNode("to my github", TextType.LINK, "https://github.com/Alexander-Plunkett"),
                TextNode(" too", TextType.TEXT)
            ]
        )

class TestTextToTextNode(unittest.TestCase):
    def test_all_text_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnode(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_no_text_type(self):
        text = "**bold** *italic* `code` ![image](image url) [link](link url)"
        self.assertEqual(
            text_to_textnode(text),
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image url"),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "link url")
            ]
        )

if __name__ == "__main__":
    unittest.main()