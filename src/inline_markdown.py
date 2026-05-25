from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.PLAIN or delimiter not in node.text:
            new_nodes.append(node)
        else:
            split_nodes = node.text.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise Exception(f"Invalid markdown syntax: no closing {delimiter} within \"{node.text}\"")
            for i in range(len(split_nodes)):
                if split_nodes[i]:
                    new_type = node.text_type if i % 2 == 0 else text_type
                    new_nodes.append(TextNode(split_nodes[i], new_type))
    return new_nodes


