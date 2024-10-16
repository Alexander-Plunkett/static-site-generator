from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        super().__init__(tag, value, props = props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Leaf nodes must have a value")

        if self.tag == None:
            return f"{self.value}"
        elif self.props != None:
            return f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'
        return f'<{self.tag}>{self.value}</{self.tag}>'