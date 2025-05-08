from replicate_folder import remove_folders, replicate_folder
from generate_webpage import generate_pages_recursive

import sys


static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template_path = "./template.html"


def main():
    if len(sys.argv) == 1:
        basepath = "/"
    else:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    remove_folders(public_dir)

    print("Copying static files to public directory...")
    replicate_folder(static_dir, public_dir)

    print("Generating webpage...")
    generate_pages_recursive(
        basepath,
        content_dir,
        template_path,
        public_dir,
    )


main()
