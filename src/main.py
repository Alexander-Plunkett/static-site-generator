import os, shutil

from copystatic import copy_contents
from page_generation import generate_pages_recursive

def main():
    dir_path_static = "./static"
    dir_path_public = "./public"
    dir_path_content = "./content"
    template_path = "./template.html"

    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    copy_contents(dir_path_static, dir_path_public)
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

main()