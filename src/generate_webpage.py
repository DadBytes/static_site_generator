import os

from markdown_to_html import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        if line.startswith("# "):
            return line.strip()[2:]
    else:
        raise ValueError("markdown is missing a h1 header")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating web page from {from_path} to {dest_path}...")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    nodes = markdown_to_html_node(markdown)
    html_content = nodes.to_html()

    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    with open(dest_path, "w") as f:
        f.write(template)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        if not os.path.isfile(f"{dir_path_content}/{item}"):
            os.mkdir(f"{dest_dir_path}/{item}")
            generate_pages_recursive(
                f"{dir_path_content}/{item}", template_path, f"{dest_dir_path}/{item}"
            )
        else:
            generate_page(
                f"{dir_path_content}/{item}",
                template_path,
                f"{dest_dir_path}/index.html",
            )
