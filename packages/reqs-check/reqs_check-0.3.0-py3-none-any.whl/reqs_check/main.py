import typer
from typing import List
from pathlib import Path
from tabulate import tabulate
from .diff import compare_requirements, filter_differences, highlight_differences
from .duplicates import find_duplicates
from .version import get_latest_versions, update_requirements_file
from .lint import lint_requirements

app = typer.Typer()


@app.command()
def check(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Paths to the requirements.txt files",
    ),
    diff: bool = typer.Option(False, "--diff", help="Show diff between files"),
    duplicates: bool = typer.Option(
        False, "--duplicates", help="Find duplicate packages in the dependencies files"
    ),
):
    """
    Check requirements files for differences or duplicates.
    """
    if duplicates:
        all_duplicates = find_duplicates(files)
        if all_duplicates:
            for file, dups in all_duplicates.items():
                typer.echo(f"🚫 Duplicates in {file}:")
                for pkg, vers in dups.items():
                    typer.echo(f"  {pkg}:")
                    for ver, line_num in vers:
                        typer.echo(f"    - {ver} (line {line_num})")
                typer.echo()
        else:
            typer.echo("✅ No duplicate packages found.")
        return

    if diff:
        if len(files) < 2:
            typer.echo("🚫 Please provide at least two files to compare.", err=True)
            raise typer.Exit(code=1)

        comparison_df = compare_requirements(files)
        filtered_df = filter_differences(comparison_df)
        highlighted_df = highlight_differences(filtered_df)
        typer.echo(
            "\n"
            + tabulate(
                highlighted_df.to_dict(orient="records"),
                headers="keys",
                tablefmt="grid",
            )
        )
    else:
        typer.echo("🚫 Please specify either --diff or --duplicates option.")


@app.command()
def lint(
    files: List[Path] = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        help="Paths to the requirements.txt files",
    ),
):
    """
    Lint the requirements files for best practices.
    """
    for file in files:
        issues = lint_requirements(file)
        if issues:
            typer.echo(f"🚫 Issues found in {file}:")
            for issue in issues:
                typer.echo(f"  - {issue}")
        else:
            typer.echo(f"✅ No issues found in {file}")


@app.command()
def versions(
    target: str = typer.Argument(
        ..., help="Path to the requirements.txt file or package name"
    ),
    fix: bool = typer.Option(
        False,
        "--fix",
        "-f",
        help="Update the file with the latest versions of unversioned packages",
    ),
    add: str = typer.Option(
        None,
        "--add",
        "-a",
        help="Add packages with their latest versions to the requirements file",
    ),
):
    """
    Check the latest version of packages or update/add packages in a requirements file.
    """

    target_path = Path(target)
    if target_path.is_file():
        if fix:
            updated = update_requirements_file(target_path, unversioned_only=True)
            unversioned = updated.keys()
            package = "package" if len(unversioned) == 1 else "packages"
            if updated:
                typer.echo(f"✅ Fixed {len(updated)} {package} in {target_path}:")
                for pkg, version in updated.items():
                    typer.echo(f"  {pkg}=={version}")
            else:
                typer.echo(
                    "✅ No packages were fixed. The packages are already versioned in the file."
                )
                typer.echo(
                    "💡 Use the option `--add` to add versioned packages in your requirements file:"
                )
                typer.echo(
                    "    `reqs-check versions {target_path} --add requests,bson`"
                )
        elif add:
            added = update_requirements_file(
                target_path, packages_to_add=add.split(","), unversioned_only=True
            )
            package = "package" if len(added) == 1 else "packages"
            if added:
                typer.echo(f"✅ Added {len(added)} {package} to {target_path}:")
                for pkg, version in added.items():
                    typer.echo(f"  {pkg}=={version}")
            else:
                typer.echo(
                    "✅ No packages were added. The packages are already in the file."
                )
        else:
            latest = get_latest_versions(target_path)
            unversioned = latest.keys()
            be = "package" if len(unversioned) == 1 else "packages"
            if latest:
                typer.echo(
                    f"🚫 Found {len(unversioned)} unversioned {be} in {target_path}:"
                )
                for pkg in unversioned:
                    typer.echo(f"  {pkg}")
                typer.echo(
                    "💡 Use the option `--fix` to update the unversioned packages in the file:"
                )
                typer.echo(f"    `reqs-check versions {target_path} --fix`")
            else:
                typer.echo(f"✅ All packages are versioned in {target_path}")
    else:
        versions = get_latest_versions(target.split(","))
        if versions:
            typer.echo("📋 Latest versions for packages:")
            for pkg, version in versions.items():
                typer.echo(f"   {pkg}=={version}")
        else:
            typer.echo(f"🚫 Failed to retrieve the latest version for {target}")


if __name__ == "__main__":
    app()
