import os
import re
import requests
from typing import Optional, Tuple


def parse_requirements(file_path) -> dict:
    """
    Parse a requirements file and return a dictionary of packages and versions.

    Args:
        file_path (str): The path to the requirements file.

    Returns:
        dict: A dictionary where the keys are package names and the values are lists of tuples (version, line_number).
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    requirements = {}
    with open(file_path, "r") as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            if line and not line.startswith("#"):
                match = re.match(r"([a-zA-Z0-9_-]+)([>=<~!]+[a-zA-Z0-9._-]+)?", line)
                if match:
                    pkg = match.group(1)
                    ver = match.group(2) if match.group(2) else "Any"
                    if pkg not in requirements:
                        requirements[pkg] = []
                    requirements[pkg].append((ver.strip(), line_number))
    return requirements


def get_latest_version(package_name: str) -> Optional[str]:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data["info"]["version"]
    except requests.RequestException:
        return None


def check_line(package_line: str) -> Tuple[Optional[str], bool]:
    """
    Check if a package is versioned and get the latest version if it's not.

    Args:
        package_line (str): A line from the requirements file.

    Returns:
        tuple[Optional[str], bool]: Package name and a boolean indicating if it is unversioned.
    """
    package_pattern = r"^([a-zA-Z0-9_.-]+)\s*([<>=!~]+.*)?$"
    match = re.match(package_pattern, package_line.strip())
    if not match:
        return None, False

    package_name = match.group(1)
    version_specifier = match.group(2)
    version_symbols = ["==", ">", "<", ">=", "<=", "!=", "~="]
    is_unversioned = not (
        version_specifier
        and any(symbol in version_specifier for symbol in version_symbols)
    )
    return package_name, is_unversioned
