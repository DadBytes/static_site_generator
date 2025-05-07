import shutil
import os


def replicate_folder(path: str, new_path: str):
    dir_list = os.listdir(path)
    for item in dir_list:
        if not os.path.isfile(f"{path}/{item}"):
            os.mkdir(f"{new_path}/{item}")
            replicate_folder(f"{path}/{item}", f"{new_path}/{item}")
        else:
            shutil.copy(f"{path}/{item}", f"{new_path}")


def clean_folders(folder_to_clean):
    shutil.rmtree(folder_to_clean, ignore_errors=True)
    os.mkdir(folder_to_clean)
