import re
from enum import Enum

from textnode import text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnode
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def markdown_to_html_node(markdown):
    blocks_md = markdown_to_blocks(markdown)
    blocks_html = []
    for block in blocks_md:
        block_type = block_to_block_type(block)
        block_node = block_to_html(block, block_type)
        blocks_html.append(block_node)
    return ParentNode("div", blocks_html)

def block_to_block_type(block):
    lines = block.split("\n")

    if re.match(r"^(#){1,6} ", block):
        return BlockType.HEADING
    
    if len(lines) > 1 and re.match(r"^(```)$", lines[0]) and re.match(r"^(```)$", lines[-1]):
        return BlockType.CODE
    
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH

def block_to_html(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(block)
        return ParentNode("p", children)
    elif block_type == BlockType.HEADING:
        children = text_to_children(block.lstrip("# "))
        tag = heading_counter(block)
        return ParentNode(tag, children)
    elif block_type == BlockType.CODE:
        children = text_to_children(f"`{block.strip("`")}`")
        return ParentNode("pre", children)
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        stripped_lines = list(map(lambda line: line.lstrip("> "), lines))
        stripped_block = "\n".join(stripped_lines)
        children = text_to_children(stripped_block)
        return ParentNode("blockquote", children)
    elif block_type == BlockType.ULIST:
        children = []
        lines = block.split("\n")
        for line in lines:
            grandchildren = text_to_children(line[2:])
            children.append(ParentNode("li", grandchildren))
        return ParentNode("ul", children)
    elif block_type == BlockType.OLIST:
        children = []
        lines = block.split("\n")
        for line in lines:
            grandchildren = text_to_children(line[3:])
            children.append(ParentNode("li", grandchildren))
        return ParentNode("ol", children)
    
def text_to_children(text):
    textnodes = text_to_textnode(text)
    HTMLnodes = list(map(text_node_to_html_node, textnodes))
    return HTMLnodes


def heading_counter(block):
    for i in range(7):
        if block[i] != "#":
            return f"h{i}"