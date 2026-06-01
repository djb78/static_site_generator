import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHtml(unittest.TestCase):
    def test_empty(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_paragraph(self):
        md = "this is a **simple** one line paragraph"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>this is a <b>simple</b> one line paragraph</p></div>") 

    def test_heading(self):
        md = "### This is a _heading_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>This is a <i>heading</i></h3></div>") 
    
    def test_quote(self):
        md = ">first line of a quote\n> second line with a space"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>first line of a quote\nsecond line with a space</blockquote></div>")

    def test_ul(self):
        md = "- this\n- list\n- is\n- unordered"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>this</li><li>list</li><li>is</li><li>unordered</li></ul></div>")

    def test_ol(self):
        md = "1. this\n2. list\n3. is\n4. ordered"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>this</li><li>list</li><li>is</li><li>ordered</li></ol></div>")

    def test_ul_inline(self):
        md = "- this **BOLD**\n- list\n- is _unordered_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>this <b>BOLD</b></li><li>list</li><li>is <i>unordered</i></li></ul></div>")

    def test_ol_inline(self):
        md = "1. this\n2. **list**\n3. is _ordered_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>this</li><li><b>list</b></li><li>is <i>ordered</i></li></ol></div>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


    def test_codeblock(self):
        md = """
    ```
This is text that _should_ remain
the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

if __name__ == "__main__":
    unittest.main()
