import os

def create_env(paths: list[str]) -> None:
    """
    Creates the paths provided. (list)
    
    :param paths: The paths to create.
    """
    for path in list(paths):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except Exception as e:
                raise Exception(f"There was an exception while creating the path '{path}'! --> {e}")

def create_standard_env() -> None:
    """
    Creates the standard paths for the project.
    (env, env/logs, env/data, env/images, env/func)
    """
    paths = [
        "env",
        "env/logs",
        "env/data",
        "env/images",
        "env/func",
    ]

    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)