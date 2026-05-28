import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN or delimiter not in node.text:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise ValueError(f"Invalid markdown syntax: no closing {delimiter} within \"{node.text}\"")
            for i in range(len(split_nodes)):
                if split_nodes[i]:
                    new_type = node.text_type if i % 2 == 0 else text_type
                    new_nodes.append(TextNode(split_nodes[i], new_type))
    return new_nodes

def extract_markdown_images(raw_md):
    # ![alt text](url)
    # return [('alt text', 'url')]
    pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    image_attributes = re.findall(pattern, raw_md)
    return image_attributes

def extract_markdown_links(raw_md):
    # [anchor_text](url)
    # return [('anchor text', 'url')]
    pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    link_attributes = re.findall(pattern, raw_md)
    return link_attributes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_url(old_nodes, TextType.IMAGE)
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        image_tuples = extract_markdown_images(node.text)
        if node.text_type != TextType.PLAIN or not image_tuples:
            new_nodes.append(node)
            continue
        
        alt_text, url = image_tuples[0]
        image_node = TextNode(alt_text, TextType.IMAGE, url)
        other_nodes = node.text.split(f"![{alt_text}]({url})", 1)

        if other_nodes[0]:
            new_nodes.append(TextNode(other_nodes[0], node.text_type))
        new_nodes.append(image_node)
        if other_nodes[1]:
            new_nodes.extend(split_nodes_image([TextNode(other_nodes[1], node.text_type)]))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_url(old_nodes, TextType.LINK)
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        link_tuples = extract_markdown_links(node.text)
        if node.text_type != TextType.PLAIN or not link_tuples:
            new_nodes.append(node)
            continue

        anchor_text, url = link_tuples[0]
        link_node = TextNode(anchor_text, TextType.LINK, url)
        other_nodes = node.text.split(f"[{anchor_text}]({url})", 1)

        if other_nodes[0]:
            new_nodes.append(TextNode(other_nodes[0], node.text_type))
        new_nodes.append(link_node)
        if other_nodes[1]:
            new_nodes.extend(split_nodes_link([TextNode(other_nodes[1], node.text_type)]))
    return new_nodes

def split_nodes_url(old_nodes: list[TextNode], url_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        
        i = ""
        if url_type == TextType.IMAGE:
            tuples = extract_markdown_images(node.text)
            i = "!"
        elif url_type == TextType.LINK:
            tuples = extract_markdown_links(node.text)
        
        if node.text_type != TextType.PLAIN or not tuples:
            new_nodes.append(node)
            continue

        text, url = tuples[0]
        url_node = TextNode(text, url_type, url)
        other_nodes = node.text.split(f"{i}[{text}]({url})", 1)

        if other_nodes[0]:
            new_nodes.append(TextNode(other_nodes[0], node.text_type))
        new_nodes.append(url_node)
        if other_nodes[1]:
            new_nodes.extend(split_nodes_url([TextNode(other_nodes[1], node.text_type)], url_type))
    return new_nodes


# images
r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# regular links
r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"