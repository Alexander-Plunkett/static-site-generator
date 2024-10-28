import os, shutil

from textnode import TextNode, TextType

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    src_root = "static"
    dst_root = "public"
    copy_contents(src_root, dst_root)

def copy_contents(src, dst, init = True):
    if init == True:
        shutil.rmtree(dst)
        os.mkdir(dst)

    if not os.path.exists(src):
        raise ValueError("No such path exists")
    
    for item in os.listdir(src):
        new_src = os.path.join(src, item)
        if "." in item:
            shutil.copy(new_src, dst)
        else:
            new_dst = os.path.join(dst, item)
            os.mkdir(new_dst)
            copy_contents(new_src, new_dst, False)

main()