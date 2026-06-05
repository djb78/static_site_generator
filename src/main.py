import os, shutil
from markdown_to_html import markdown_to_html_node
from block_markdown import extract_title

def copy_directory(source, destination):
    # make sure source is valid
    if not os.path.exists(source):
        raise Exception(f"invalid directory: {source}")
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    
    for child in os.listdir(source):
        child_path = os.path.join(source, child)
       
        if os.path.isfile(child_path):
            # copy to destination
            shutil.copy(child_path, destination)
        else:
            # assume directory
            destination_path = os.path.join(destination, child)
            os.mkdir(destination_path)
            copy_directory(child_path, destination_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = template = ""
    try:
        with open(from_path, 'r') as f:
            markdown_file = f.read()
        with open(template_path, 'r') as f:
            template = f.read()
    except FileNotFoundError:
        pass

    if not markdown_file: raise Exception(f"missing content: {from_path}")
    if not template: raise Exception(f"missing template: {template_path}")
    
    title = extract_title(markdown_file)
    html_file = markdown_to_html_node(markdown_file).to_html()
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_file)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)
    try:
        with open(dest_path, "w") as f:
            f.write(page)
    except FileNotFoundError:
        raise Exception(f"could not write to {dest_path}")

def main():
    copy_directory("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
    generate_page("content/contact/index.md", "template.html", "public/contact/index.html")
    generate_page("content/blog/glorfindel/index.md", "template.html", "public/blog/glorfindel/index.html")
    generate_page("content/blog/majesty/index.md", "template.html", "public/blog/majesty/index.html")
    generate_page("content/blog/tom/index.md", "template.html", "public/blog/tom/index.html")

if __name__ == "__main__":
    main()