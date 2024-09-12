from .utils import parse_requirements


def find_duplicates(files):
    """
    Find duplicate packages in multiple requirements files.

    Args:
        files (list): A list of file paths to requirements files.

    Returns:
        dict: A dictionary where the keys are file paths and the values are dictionaries of duplicate packages and versions.
    """
    all_duplicates = {}

    for file in files:
        requirements = parse_requirements(file)
        duplicates = {pkg: vers for pkg, vers in requirements.items() if len(vers) > 1}
        if duplicates:
            all_duplicates[file] = duplicates

    return all_duplicates
