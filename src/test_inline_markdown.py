import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestMarkdownToText(unittest.TestCase):
    # split_nodes_delimiter
    def test_split_nodes_bold(self):
        bold_node = TextNode("plain text, **this text is bold**", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([bold_node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_nodes_italic(self):
        italic_node = TextNode("plain text, _italic text_", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([italic_node], '_', TextType.ITALIC)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_split_nodes_code(self):
        code_node = TextNode("plain text, ```code text```", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([code_node], '```', TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_split_nodes_plain(self):
        plain_node = TextNode("plain node, just text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([plain_node], 'b', TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "plain node, just text")
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)

    def test_split_nodes_multi(self):
        bold_node = TextNode("plain text, **this text is bold**", TextType.PLAIN)
        double_bold_node = TextNode("plain text **bold1** plain text **bold2**", TextType.PLAIN)
        plain_node = TextNode("plain node, just text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([bold_node, plain_node, double_bold_node], '**', TextType.BOLD)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text_type, TextType.PLAIN)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    # extract_markdown_images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/image.jpeg)")
        self.assertEqual([("image", "https://i.imgur.com/image.jpeg")], matches)

    # extract_markdown_links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link[anchor](https://i.dont.know)")
        self.assertEqual([("anchor", "https://i.dont.know")], matches)
        
if __name__ == "__main__":
    unittest.main()