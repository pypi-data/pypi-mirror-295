from pathlib import Path
from typing import List, Dict, Optional
import typer
from .utils import get_latest_version, check_line


def get_latest_versions(packages):
    """
    Get the latest versions of the packages.

    Args:
        packages (list, str): A list of package names or requirements file path.
        only_unversioned (bool): If True, only unversioned packages in the requirements file are checked, else all packages are checked. Cannot be used if packages is a list.


    Returns:
        dict: A dictionary with the package names as keys and the latest versions as values.


    """

    if isinstance(packages, (str, Path)):
        with open(packages, "r") as file:
            packages = [
                line.strip()
                for line in file
                if check_line(line)[1] and not line.strip().startswith("#")
            ]
    return {package: get_latest_version(package) for package in packages}


def update_requirements_file(
    file_path: Path,
    packages_to_add: Optional[List[str]] = None,
    unversioned_only: bool = False,
) -> Dict[str, str]:
    """
    Update a requirements file with latest versions and/or add new packages.

    Args:
        file_path (Path): Path to the requirements file.
        packages_to_add (Optional[List[str]]): List of packages to add if not present.
        unversioned_only (bool): If True, only update packages without version specifiers.

    Returns:
        Dict[str, str]: A dictionary of updated/added packages and their versions.
    """
    updated_packages = {}
    existing_packages = set()
    updated_lines = []

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            package_name, is_unversioned = check_line(line)
            if not package_name:
                updated_lines.append(line)
                continue

            existing_packages.add(package_name)

            if unversioned_only and not is_unversioned:
                updated_lines.append(line)
                continue

            latest_version = get_latest_version(package_name)
            if latest_version:
                updated_line = f"{package_name}=={latest_version}"
                updated_lines.append(updated_line)
                updated_packages[package_name] = latest_version
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    if packages_to_add:
        for package in packages_to_add:
            if package not in existing_packages:
                latest_version = get_latest_version(package)
                if latest_version:
                    updated_lines.append(f"{package}=={latest_version}")
                    updated_packages[package] = latest_version
                else:
                    typer.echo(
                        f"🚫 {package} not found. Please check the package name."
                    )
                    exit(0)

    with open(file_path, "w") as file:
        file.write("\n".join(updated_lines))

    return updated_packages
