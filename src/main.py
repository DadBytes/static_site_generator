from replicate_folder import remove_folders, replicate_folder
from generate_webpage import generate_pages_recursive

import sys


static_dir = "./static"
docs_dir = "./docs"
content_dir = "./content"
template_path = "./template.html"


def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    remove_folders(docs_dir)

    print("Copying static files to public directory...")
    replicate_folder(static_dir, docs_dir)

    print("Generating webpage...")
    generate_pages_recursive(
        basepath,
        content_dir,
        template_path,
        docs_dir,
    )


main()
