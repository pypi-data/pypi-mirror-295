from reqs_check.version import (
    get_latest_versions,
    update_requirements_file,
    get_latest_version,
)
import re
from pathlib import Path


def test_get_latest_version():
    # check that it returns a version number like using pattern regex
    latest_version = get_latest_version("requests")
    if latest_version is not None:
        assert re.match(r"\d+\.\d+\.\d+", latest_version)


def test_get_latest_versions():
    # check that it returns a dictionary with the package name as key and the version as value
    latest_versions = get_latest_versions(["requests"])
    assert isinstance(latest_versions, dict)
    assert len(latest_versions) == 1
    assert "requests" in latest_versions
    latest_version = latest_versions["requests"]
    if latest_version is not None:
        assert re.match(r"\d+\.\d+\.\d+", latest_version)

    # check for multiple packages
    latest_versions_multiple = get_latest_versions(["requests", "bson"])
    assert isinstance(latest_versions_multiple, dict)
    assert len(latest_versions_multiple) == 2
    assert "requests" in latest_versions_multiple
    assert "bson" in latest_versions_multiple

    if latest_versions_multiple["requests"] is not None:
        assert re.match(r"\d+\.\d+\.\d+", latest_versions_multiple["requests"])
    if latest_versions_multiple["bson"] is not None:
        assert re.match(r"\d+\.\d+\.\d+", latest_versions_multiple["bson"])


def test_update_requirements_file_fix():
    # create a temporary file
    file_path = Path("requirements.txt")
    file_path.write_text("requests==2.28.1\nbson==0.5.9\npandas\nnumpy")

    update_requirements_file(file_path, unversioned_only=True)

    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "pandas" in line:
                assert line.split("==")[1].strip() == get_latest_version("pandas")
            if "numpy" in line:
                assert line.split("==")[1].strip() == get_latest_version("numpy")


def test_update_requirements_file_add():
    file_path = Path("requirements.txt")
    file_path.write_text("requests==2.28.1\nbson==0.5.9")

    # update the file
    update_requirements_file(file_path, packages_to_add=["pandas", "numpy"])

    # check that pandas and numpy are in the file
    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "pandas" in line:
                assert line.split("==")[1].strip() == get_latest_version("pandas")
            if "numpy" in line:
                assert line.split("==")[1].strip() == get_latest_version("numpy")


def test_update_requirements_file_add_and_fix():
    # create a temporary file
    file_path = Path("requirements.txt")
    file_path.write_text("requests==2.28.1\nbson==0.5.9\npandas\nnumpy")

    # update the file
    update_requirements_file(
        file_path, packages_to_add=["pymongo", "fastapi"], unversioned_only=True
    )

    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "pymongo" in line:
                assert line.split("==")[1].strip() == get_latest_version("pymongo")
            if "fastapi" in line:
                assert line.split("==")[1].strip() == get_latest_version("fastapi")
            if "pandas" in line:
                assert line.split("==")[1].strip() == get_latest_version("pandas")
            if "numpy" in line:
                assert line.split("==")[1].strip() == get_latest_version("numpy")


def test_update_requirements_file_all():
    # create a temporary file
    file_path = Path("requirements.txt")
    file_path.write_text("requests==2.28.1\nbson==0.5.9\npandas\nnumpy")

    update_requirements_file(
        file_path, packages_to_add=["pymongo", "fastapi"], unversioned_only=False
    )

    with open(file_path, "r") as file:
        lines = file.readlines()
        for line in lines:
            if "requests" in line:
                assert line.split("==")[1].strip() == get_latest_version("requests")
            if "bson" in line:
                assert line.split("==")[1].strip() == get_latest_version("bson")
            if "pymongo" in line:
                assert line.split("==")[1].strip() == get_latest_version("pymongo")
            if "fastapi" in line:
                assert line.split("==")[1].strip() == get_latest_version("fastapi")
            if "pandas" in line:
                assert line.split("==")[1].strip() == get_latest_version("pandas")
            if "numpy" in line:
                assert line.split("==")[1].strip() == get_latest_version("numpy")
