from enum import Enum

class TextType(Enum):
    PLAIN = "plain" #"text"
    BOLD = "bold" #"**text**"
    ITALIC = "italic" #"_text_"
    CODE = "code" #"'text'"
    LINK = "link" #"[text](url)"
    IMAGE = "image" #"![text](url)"

'''
inline_types = Enum('TextType', [
    'PLAIN',
    'BOLD',
    'ITALIC'
    'CODE'
    'LINK'
    'IMAGE'
])
'''

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


