import re

from textnode import TextNode, TextType

def text_to_textnode(text):
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        split_nodes = []
        blocks = node.text.split(delimiter)
        if len(blocks) % 2 == 0:
            raise ValueError("Invalid markdown, formatted phrase not closed")

        for i in range(len(blocks)):
            if blocks[i] == "":
                continue
            elif i % 2 == 0:
                split_nodes.append(TextNode(blocks[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(blocks[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        text = node.text
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        split_nodes = []
        for i in range(len(images)):
            blocks = text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if len(blocks) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if blocks[0] != "":
                split_nodes.append(TextNode(blocks[0], TextType.TEXT))
            split_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            text = blocks[1]
        if text != "":
            split_nodes.append(TextNode(blocks[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            new_nodes.append(node)
            continue
        text = node.text
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        split_nodes = []
        for i in range(len(links)):
            blocks = text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if len(blocks) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if blocks[0] != "":
                split_nodes.append(TextNode(blocks[0], TextType.TEXT))
            split_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            text = blocks[1]
        if text != "":
            split_nodes.append(TextNode(blocks[1], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r" \[(.*?)\]\((.*?)\)", text)