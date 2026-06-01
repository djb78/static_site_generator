class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html = ''
        if self.props is not None:
            for prop in self.props:
                html += f' {prop}="{self.props[prop]}"'
        return html
    
    def __repr__(self):
        # return f"tag:{self.tag}\nvalue:{self.value}\nchildren:{self.children}\nprops:{self.props}"
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"no value: {self.__repr__}")
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        # return f"tag:{self.tag}\nvalue:{self.value}\nprops:{self.props}"
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("no tag")
        if self.children is None:
            raise ValueError("no children")
    
        node_html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            node_html += child.to_html()
        node_html += f"</{self.tag}>"

        return node_html