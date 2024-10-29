import os

from markdown_blocks import markdown_to_html_node, markdown_to_blocks

def extract_title(markdown):
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return (block.lstrip("# ")).rstrip(" ")
    raise Exception("No h1 title in markdown, cannot be extracted")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path, "r").read()
    template = open(template_path, "r").read()

    node = markdown_to_html_node(markdown)
    raw_html = node.to_html()
    html_title = extract_title(markdown)

    added_title = template.replace("{{ Title }}", html_title)
    new_file = added_title.replace("{{ Content }}", raw_html)

    dir_path = os.path.dirname(dest_path)

    os.makedirs(dir_path, exist_ok=True)
    open(dest_path, "w").write(new_file)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        if ".md" in item:
            generate_page(
                os.path.join(dir_path_content, item),
                template_path, 
                os.path.join(dest_dir_path, f"{item[:-2]}html")
            )
        elif "." not in item:
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path, 
                os.path.join(dest_dir_path, item)
            )