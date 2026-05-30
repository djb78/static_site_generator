

def markdown_to_blocks(markdown):
    # input: raw markdown string, full document [well-writen]
    # return ["block strings"]
    blocks = []
    parts = markdown.split('\n\n')
    for part in parts:
        if part == '': continue
        blocks.append(part.strip())
    return blocks
