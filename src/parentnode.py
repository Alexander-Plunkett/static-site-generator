from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag = None, children = None, props = None):
        super().__init__(tag, children = children, props = props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent nodes must have a tag")
        elif self.children == None:
            raise ValueError("Parent nodes must have children")

        child_html = ""
        for child in self.children:
            child_html += child.to_html()

        if self.props != None:
            return f'<{self.tag}{super().props_to_html()}>{child_html}</{self.tag}>'
        return f'<{self.tag}>{child_html}</{self.tag}>'