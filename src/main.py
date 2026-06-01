import os, shutil
from textnode import TextNode

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

def main():
    node = TextNode("dummy text", "link", "https://wtf.com")
    print(node)
    copy_directory("static", "public")

if __name__ == "__main__":
    main()
