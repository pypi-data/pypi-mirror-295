import git
from pathlib import Path
import configparser


def get_project_root():
    """
    Get the root directory of the project.

    :return: The root directory of the project.
    """
    return Path(git.Repo('.', search_parent_directories=True).working_tree_dir)


def load_credentials(credentials_path):
    """
    Load the credentials from the config file.

    :return: The credentials loaded from the config file.
    """
    dbconfig = configparser.ConfigParser(interpolation=None)
    dbconfig.read(credentials_path)
    return dbconfig