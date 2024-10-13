class TextNode():
    def __init__(self, text, type, url):
        self.text = text
        self.text_type = type
        self.url = url

    def __eq__(self, comparison):
        if self.text == comparison.text and self.text_type == comparison.text_type and self.url == comparison.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"