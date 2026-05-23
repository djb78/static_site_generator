import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    '''
    def test_props_to_html(self):
        node = HTMLNode(props={'href':'www.wut.tf'})
        print(node)
    '''
        
    def test_multi_prop_html(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_single_prop_html(self):
        node = HTMLNode("a", "click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')

    def test_none_prop_html(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), '')

    def test_empty_prop_html(self):
        node = HTMLNode("p", "hello", None, {})
        self.assertEqual(node.props_to_html(), '')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()