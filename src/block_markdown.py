# import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "pparagraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    # markdown: raw markdown string, full document [well-writen]
    # return ["block strings"]
    blocks = []
    parts = markdown.split('\n\n')
    for part in parts:
        if part == '': continue
        blocks.append(part.strip())
    return blocks

def block_to_blocktype(block):
    # block: string representing a single block w/o leading/trailing whitespace
    # return BlockType

    # heading
    first_word = block.split(' ', 1)[0]
    if 1 <= len(first_word) <= 6 and all(c == '#' for c in first_word): return BlockType.HEADING
    # code
    if block.startswith("```") and '\n' in block and block.endswith("```"): return BlockType.CODE
    # quote
    lines = block.splitlines()
    if all(line.startswith(">") for line in lines): return BlockType.QUOTE
    # unordered list
    if all(line.startswith("- ") for line in lines): return BlockType.UNORDERED_LIST
    # ordered list
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)): return BlockType.ORDERED_LIST
    # paragraph
    return BlockType.PARAGRAPH
