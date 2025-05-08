import shutil
import os


def replicate_folder(source: str, destination: str):
    if not os.path.exists(destination):
        os.mkdir(destination)
    dir_list = os.listdir(source)
    for item in dir_list:
        if not os.path.isfile(f"{source}/{item}"):
            os.mkdir(f"{destination}/{item}")
            replicate_folder(f"{source}/{item}", f"{destination}/{item}")
        else:
            shutil.copy(f"{source}/{item}", f"{destination}")


def remove_folders(folder_to_clean):
    if os.path.exists(folder_to_clean):
        shutil.rmtree(folder_to_clean, ignore_errors=True)
