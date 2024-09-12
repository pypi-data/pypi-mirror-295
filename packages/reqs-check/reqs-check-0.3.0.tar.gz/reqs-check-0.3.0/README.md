
# reqs-check

`reqs-check` is a tool to check and compare dependencies files(requirements.txt, pyproject.toml, etc...) for Python projects.


## Installation

To install `reqs-check`, use `pip`:

```sh
pip install reqs-check
```

## Usage
```
 Usage: reqs-check [OPTIONS] COMMAND [ARGS]...                                                                       
                                                                                                                     
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                           │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.    │
│ --help                        Show this message and exit.                                                         │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ check      Check requirements files for differences or duplicates.                                                │
│ lint       Lint the requirements files for best practices.                                                        │
│ versions   Check the latest version of packages or update/add packages in a requirements file.                    │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
### check
```
 Usage: reqs-check check [OPTIONS] FILES...                                                                          
                                                                                                                     
 Check requirements files for differences or duplicates.                                                             
                                                                                                                     
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    files      FILES...  Paths to the requirements.txt files [default: None] [required]                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --diff                Show diff between files                                                                     │
│ --duplicates          Find duplicate packages in the dependencies files                                           │
│ --help                Show this message and exit.                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### lint
```
 Usage: reqs-check lint [OPTIONS] FILES...                                                                           
                                                                                                                     
 Lint the requirements files for best practices.                                                                     
                                                                                                                     
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    files      FILES...  Paths to the requirements.txt files [default: None] [required]                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                                                       │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### versions
````
 Usage: reqs-check versions [OPTIONS] TARGET                                                                         
                                                                                                                     
 Check the latest version of packages or update/add packages in a requirements file.                                 
                                                                                                                     
╭─ Arguments ───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    target      TEXT  Path to the requirements.txt file or package name [default: None] [required]               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --fix   -f            Update the file with the latest versions of unversioned packages                            │
│ --add   -a      TEXT  Add packages with their latest versions to the requirements file [default: None]            │
│ --help                Show this message and exit.                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````


## Examples

Let's consider the following files: 

**requirements1.txt**
```
pandas==1.1.5
numpy==1.19.5
scipy~=1.5.4
matplotlib==3.3.4
```
and 

**requirements2.txt**
```
pandas==1.1.5
numpy==1.19.3
matplotlib==3.2.1
requests>=2.24.0
scipy==1.5.4
numpy==1.19
requests
```
### Compare requirements files

> **Note:** The files are in the directory `examples/` of the github repository.

This command compares two `requirements.txt` files and highlights the differences.

```shell
reqs-check check requirements1.txt requirements2.txt
```
**Output:**
```
+------------+---------------------+---------------------+
| Package    | requirements1.txt   | requirements2.txt   |
+============+=====================+=====================+
| numpy      | ==1.19.5            | ==1.19.3            |
+------------+---------------------+---------------------+
| scipy      | ~=1.5.4             | ==1.5.4             |
+------------+---------------------+---------------------+
| matplotlib | ==3.3.4             | ==3.2.1             |
+------------+---------------------+---------------------+
| requests   | Not Present         | >=2.24.0            |
+------------+---------------------+---------------------+
```
> **Note:** The values are color-coded for better readability in the terminal.


### Find duplicates in requirements files

This command finds duplicated packages in the `requirements.txt` files(at least one).

```shell
reqs-check check --duplicates requirements1.txt requirements2.txt
```
**Output:**
```
🚫 Duplicates in requirements2.txt:
  numpy:
    - ==1.19.3 (line 2)
    - ==1.19 (line 6)
  requests:
    - >=2.24.0 (line 4)
    - Any (line 7)
````
You can see that the output shows the duplicated packages in the second file `requirements2.txt` while the first file `requirements1.txt` has no duplicated packages.

For the next examples, let's consider the following file:

**requirements3.txt**
```
pandas==1.1.5
numpy==1.19.5
scipy~=1.5.4
matplotlib==3.3.4
pandas
numpy>=1.15
-e git+https://github.com/user/repo.git#egg=package
```

### Lint requirements files

This command checks a `requirements.txt` file for best practices, such as specifying version numbers and avoiding editable installs.

```sh
reqs-check lint requirements3.txt 
```
```
🚫 Issues found in requirements3.txt:
  - Line 5: 'pandas' does not specify a version.
  - Line 7: '-e git+https://github.com/user/repo.git#egg=package' does not specify a version.
  - Line 7: '-e git+https://github.com/user/repo.git#egg=package' uses editable installs, which are not recommended for production.
```

### Check and update packages versions

- Check the latest version of packages that you specify(comma separated)


  ```sh
  reqs-check versions pandas,requests
  ```
    **Output:**
  ```
  📋 Latest versions for packages:
    pandas==2.2.2
    requests==2.32.3

  ```
- Check if there are any unversioned packages in the requirements file:
  ```shell
  reqs-check versions requirements3.txt
  ```
  **Output:**
  ```
  🚫 Found 1 unversioned package in requirements3.txt:
    pandas
  💡 Use the option `--fix` to update the unversioned packages in the file:
      `reqs-check versions requirements3.txt --fix`
  ```
### Update requirements file with the latest versions
- Fix unversioned packages in a requirements file:
  ```shell
  reqs-check versions requirements3.txt --fix
  ```
  **Output:**
  ```
  ✅ Fixed 1 package in requirements3.txt:
    pandas==2.2.2
  ```
- Add versioned(with the latest version) packages in a requirements file:
  ```shell
  reqs-check versions requirements3.txt --add requests,bson
  ```
  **Output:**
  ```
  ✅ Added 3 packages to requirements3.txt:
    pandas==2.2.2
    requests==2.32.3
    bson==0.5.10
  ```


## Next Steps

We plan to add more features to `reqs-check` to resolve some use cases that we've had to deal with. 

### Planned features

- Support for additional file formats (e.g., `Pipfile`, `pyproject.toml`).

- Support for additional checks (e.g., security vulnerabilities).

- Integration with CI/CD pipelines for automated checks.

- Detailed reports in various formats (e.g., JSON, HTML).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
