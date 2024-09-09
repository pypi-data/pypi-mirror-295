import pathlib


def create_dir_if_not_exists(dir_path):
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)