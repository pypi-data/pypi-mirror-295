from reqs_check.main import app
from typer.testing import CliRunner
import tempfile


def test_check():
    runner = CliRunner()

    diff_result = runner.invoke(
        app,
        ["check", "--diff", "examples/requirements1.txt", "examples/requirements2.txt"],
    )

    assert diff_result.exit_code == 0
    assert "examples/requirements1.txt" in diff_result.output
    assert "examples/requirements2.txt" in diff_result.output
    assert "numpy" in diff_result.output
    assert "scipy" in diff_result.output
    assert "matplotlib" in diff_result.output
    assert "requests" in diff_result.output

    duplicates_result = runner.invoke(
        app,
        [
            "check",
            "--duplicates",
            "examples/requirements1.txt",
            "examples/requirements2.txt",
        ],
    )

    assert duplicates_result.exit_code == 0
    assert "examples/requirements2.txt" in duplicates_result.output
    assert "numpy" in duplicates_result.output
    assert "requests" in duplicates_result.output


def test_lint():
    runner = CliRunner()

    lint_result = runner.invoke(app, ["lint", "examples/requirements3.txt"])
    assert lint_result.exit_code == 0
    assert "examples/requirements3.txt" in lint_result.output
    assert "does not specify a version" in lint_result.output


def test_version():
    runner = CliRunner()

    version_result = runner.invoke(app, ["versions", "examples/requirements3.txt"])
    assert version_result.exit_code == 0
    assert "examples/requirements3.txt" in version_result.output
    assert "pandas" in version_result.output
    assert "Found 1 unversioned package" in version_result.output

    # create a temp file from the original
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open("examples/requirements3.txt", "r") as file:
        temp_file.write(file.read().encode())
    temp_file.close()

    # run the fix command
    fix_result = runner.invoke(app, ["versions", "--fix", temp_file.name])
    assert fix_result.exit_code == 0
    assert "pandas" in fix_result.output
    assert f"✅ Fixed 1 package in {temp_file.name}:" in fix_result.output

    # run the add command
    add_result = runner.invoke(
        app, ["versions", "--add", "bson,requests", temp_file.name]
    )
    assert add_result.exit_code == 0
    assert "bson" in add_result.output
    assert "requests" in add_result.output
    assert f"✅ Added 2 packages to {temp_file.name}:" in add_result.output
