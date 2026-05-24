import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_type_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    # to_html_node tests
    def test_text(self):
        text_node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    #bold
    def test_bold(self):
        text_node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
    #italic
    def test_italic(self):
        text_node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic node")
    #code
    def test_code(self):
        text_node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code node")
    #link
    def test_link(self):
        text_node = TextNode("This is a link node", TextType.LINK, 'https://here.is/a_link.html')
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props['href'], 'https://here.is/a_link.html')
    #image
    def test_image(self):
        text_node = TextNode("This is an image node", TextType.IMAGE, "https://here.is/an_image.gif")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['alt'], "This is an image node")
        self.assertEqual(html_node.props['src'], "https://here.is/an_image.gif")

if __name__ == "__main__":
    unittest.main()