import unittest
from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_blocktype    
)

class TestMarkdownToBlocks(unittest.TestCase):
# markdown_to_blocks
# ==================
    def test_markdown_to_blocks_multiple(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_newlines(self):
        md = """


This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items





"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_oneline(self):
        md = "This is **bolded** paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph"
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

# block_to_blocktype
# ==================
    def test_block_to_head(self):
        block = "## this is a heading"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_code(self):
        block = "```\nthis is a code block\n```"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.CODE)

    def test_block_to_quote(self):
        block = ">this is a quote"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_ul(self):
        block = "- this\n- list\n- is\n- unordered"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.UNORDERED_LIST)

    def test_block_to_ol(self):
        block = "1. this\n2. list\n3. is\n4. ordered"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.ORDERED_LIST)

    def test_block_to_paragraph(self):
        block = "this is a really short paragraph. if not for this sentence some may even just call it a sentence."
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_head_7(self):
        block = "####### that's too many #'s"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_head_6(self):
        block = "###### smallest recognizable heading"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.HEADING)

    def test_block_to_head_nospace(self):
        block = "##I need some space here"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_quote_multiline(self):
        block = "> I might be wrong\n>but i'm not lying."
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.QUOTE)

    def test_block_to_quote_multiline_missing(self):
        block = ">I might be wrong\nbut i'm not lying"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_ol_skipone(self):
        block = "2. list\n3. is\n4. ordered"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_ol_skiptwo(self):
        block = "1. this\n3. is\n4. ordered"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)

    def test_block_to_code_malformed(self):
        block = "```"
        type = block_to_blocktype(block)
        self.assertEqual(type, BlockType.PARAGRAPH)
    

if __name__ == "__main__":
    unittest.main()
