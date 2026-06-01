from block_markdown import BlockType, markdown_to_blocks, block_to_blocktype
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode, LeafNode

BLOCK_TAGS = {
    BlockType.PARAGRAPH: 'p',
    BlockType.HEADING: 'h',
    BlockType.CODE: 'code',
    BlockType.QUOTE: 'blockquote',
    BlockType.UNORDERED_LIST: 'ul',
    BlockType.ORDERED_LIST: 'ol'
}
def get_block_tag(type):
    return BLOCK_TAGS.get(type, '')

def markdown_to_html_node(md_doc):
    md_blocks = markdown_to_blocks(md_doc)
    html_blocks = []
    print(f"MD BLOCKS: {md_blocks}")
    for md_block in md_blocks:
        pre_nested = False
        html_block = child_html = child_value = None
        tag = get_block_tag(block_to_blocktype(md_block))
        match tag:
            case 'p':
                # paragraph - no cleaning needed
                child_value = " ".join(md_block.splitlines())

            case 'h':
                # header - remove #'s
                head_delimiter, child_value = md_block.split(' ', 1)
                tag += str(len(head_delimiter))
                
            case 'code':
                # code - remove ``` beginning and end
                child_value = md_block.split("```")[1].strip()+"\n"
                child_html = [LeafNode(None, child_value)]
                pre_nested = True

            case 'blockquote':
                # quote - remove ">" each line
                child_value = '\n'.join([line.split('>', 1)[1].strip() for line in md_block.splitlines()])
                
            case "ul" | "ol":
                # ul = remove "- " each line
                list_items = [line.split(' ', 1)[1] for line in md_block.splitlines()]
                li_textnodes = [text_to_textnodes(item) for item in list_items] 
                
                li_html = []
                for li in li_textnodes:
                    li_html.append("".join([text_node_to_html_node(textnode).to_html() for textnode in li]))
                child_html = [LeafNode('li', li_value) for li_value in li_html]

        if child_html is None:
            if child_value is None: continue
            child_html = [text_node_to_html_node(textnode) for textnode in text_to_textnodes(child_value)]
        if pre_nested:
            nested_node = ParentNode(tag, child_html)
            tag, child_html = 'pre', [nested_node]
        html_block = ParentNode(tag, child_html)


        if not html_block: continue
        html_blocks.append(html_block)
    return ParentNode('div', html_blocks)