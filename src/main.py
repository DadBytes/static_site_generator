from replicate_folder import clean_folders, replicate_folder
from generate_webpage import generate_pages_recursive


def main():
    folder_to_replicate = "static"
    folder_to_clean = "public"

    print("Deleting public directory...")
    clean_folders(folder_to_clean)

    print("Copying static files to public directory...")
    replicate_folder(folder_to_replicate, folder_to_clean)

    print("Generating webpage...")
    generate_pages_recursive("content", "template.html", "public")


main()
