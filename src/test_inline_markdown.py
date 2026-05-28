import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestMarkdownToText(unittest.TestCase):
    # split_nodes_delimiter
    #==========================
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
    #==========================
    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/image.jpeg)")
        self.assertEqual([("image", "https://i.imgur.com/image.jpeg")], matches)

    # extract_markdown_links
    #==========================
    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link[anchor](https://i.dont.know)")
        self.assertEqual([("anchor", "https://i.dont.know")], matches)

    # split_nodes_image
    #==========================
    def test_split_images_two(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_none(self):
        node = TextNode("These are not the images you're looking for", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("These are not the images you're looking for", TextType.PLAIN)], new_nodes)

    def test_split_images_middle(self):
        node = TextNode("one in front ![look here](http://an.image.location/image.img) and one behind", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("one in front ", TextType.PLAIN),
                TextNode("look here", TextType.IMAGE, "http://an.image.location/image.img"),
                TextNode(" and one behind", TextType.PLAIN)
            ],
            new_nodes
        )

    def test_split_images_start(self):
        node = TextNode("![look here](http://an.image.location/image.img) backend only!", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("look here", TextType.IMAGE, "http://an.image.location/image.img"),
                TextNode(" backend only!", TextType.PLAIN)
            ],
            new_nodes
        )   
    
    
    def test_split_images_end(self):
        node = TextNode("one in front ![look here](http://an.image.location/image.img)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("one in front ", TextType.PLAIN),
                TextNode("look here", TextType.IMAGE, "http://an.image.location/image.img")
            ],
            new_nodes
        )
    
    def test_split_images_adjacent(self):
        node = TextNode("![don't look over there](http://an.image.location/betterimage.img)![look here](http://an.image.location/image.img)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("don't look over there", TextType.IMAGE, "http://an.image.location/betterimage.img"),
                TextNode("look here", TextType.IMAGE, "http://an.image.location/image.img")
            ],
            new_nodes
        )

    def test_split_images_type(self):
        node = TextNode("print('hello world!')", TextType.CODE)
        new_nodes = split_nodes_image([node])
        self.assertEqual([TextNode("print('hello world!')", TextType.CODE)], new_nodes)   

    def test_split_images_mixed(self):
        image_node = TextNode("look here", TextType.IMAGE, "http://an.image.location/image.img")
        double_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        plain_node = TextNode("These are not the images you're looking for", TextType.PLAIN)
        new_nodes = split_nodes_image([image_node, double_node, plain_node])
        self.assertEqual(
            [
                TextNode("look here", TextType.IMAGE, "http://an.image.location/image.img"),
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("These are not the images you're looking for", TextType.PLAIN)
            ],
            new_nodes
        )  

    def test_split_images_invalid(self):
        node = TextNode("what does ![ do in markdown? why is ther a ( after the next ]?", TextType.PLAIN) 
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [TextNode("what does ![ do in markdown? why is ther a ( after the next ]?", TextType.PLAIN)],
            new_nodes
        )

    # split_nodes_link
    #==========================
    def test_split_links_two(self):
        node = TextNode(
            "This is text with a [link](https://a.link.location/) and another [second link](https://b.link.location/)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://a.link.location/"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second link", TextType.LINK, "https://b.link.location/"
                ),
            ],
            new_nodes,
        )

    def test_split_links_none(self):
        node = TextNode("These are not the images you're looking for", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual([TextNode("These are not the images you're looking for", TextType.PLAIN)], new_nodes)

    def test_split_links_middle(self):
        node = TextNode("one in front [click here](http://a.link.location/) and one behind", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("one in front ", TextType.PLAIN),
                TextNode("click here", TextType.LINK, "http://a.link.location/"),
                TextNode(" and one behind", TextType.PLAIN)
            ],
            new_nodes
        )

    def test_split_links_start(self):
        node = TextNode("[click here](http://a.link.location/) backend only!", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("click here", TextType.LINK, "http://a.link.location/"),
                TextNode(" backend only!", TextType.PLAIN)
            ],
            new_nodes
        )   
    
    
    def test_split_links_end(self):
        node = TextNode("one in front [click here](http://a.link.location/)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("one in front ", TextType.PLAIN),
                TextNode("click here", TextType.LINK, "http://a.link.location/")
            ],
            new_nodes
        )
    
    def test_split_links_adjacent(self):
        node = TextNode("[don't click over there](http://better.link.location/)[click here](http://a.link.location/)", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("don't click over there", TextType.LINK, "http://better.link.location/"),
                TextNode("click here", TextType.LINK, "http://a.link.location/")
            ],
            new_nodes
        )

    def test_split_links_type(self):
        node = TextNode("print('hello world!')", TextType.CODE)
        new_nodes = split_nodes_link([node])
        self.assertEqual([TextNode("print('hello world!')", TextType.CODE)], new_nodes)   

    def test_split_links_mixed(self):
        link_node = TextNode("click here", TextType.LINK, "http://a.link.location/")
        double_node = TextNode(
            "This is text with a [link](http://b.link.location/) and another [second link](http://c.link.location/)",
            TextType.PLAIN,
        )
        plain_node = TextNode("These are not the links you're looking for", TextType.PLAIN)
        new_nodes = split_nodes_link([link_node, double_node, plain_node])
        self.assertEqual(
            [
                TextNode("click here", TextType.LINK, "http://a.link.location/"),
                TextNode("This is text with a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "http://b.link.location/"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second link", TextType.LINK, "http://c.link.location/"),
                TextNode("These are not the links you're looking for", TextType.PLAIN)
            ],
            new_nodes
        )  

    def test_split_links_invalid(self):
        node = TextNode("what does [ do in markdown? why is ther a ( after the next ]?", TextType.PLAIN) 
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [TextNode("what does [ do in markdown? why is ther a ( after the next ]?", TextType.PLAIN)],
            new_nodes
        )
        
if __name__ == "__main__":
    unittest.main()