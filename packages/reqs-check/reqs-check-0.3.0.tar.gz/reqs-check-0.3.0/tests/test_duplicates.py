from reqs_check.duplicates import find_duplicates


def test_find_duplicates(tmp_path):
    req_file1 = tmp_path / "requirements1.txt"
    req_file1.write_text("pandas>=1.1.5\nnumpy==1.19.5\nnumpy==1.18.5\nscipy~=1.5.4")

    req_file2 = tmp_path / "requirements2.txt"
    req_file2.write_text(
        "pandas==1.1.5\nnumpy==1.19.3\nmatplotlib==3.3.4\nmatplotlib==3.2.1"
    )

    duplicates = find_duplicates([str(req_file1), str(req_file2)])

    assert str(req_file1) in duplicates
    assert "numpy" in duplicates[str(req_file1)]
    assert duplicates[str(req_file1)]["numpy"] == [("==1.19.5", 2), ("==1.18.5", 3)]

    assert str(req_file2) in duplicates
    assert "matplotlib" in duplicates[str(req_file2)]
    assert duplicates[str(req_file2)]["matplotlib"] == [("==3.3.4", 3), ("==3.2.1", 4)]

    # Additional assertions
    assert "pandas" not in duplicates[str(req_file1)]
    assert "scipy" not in duplicates[str(req_file1)]
    assert "numpy" not in duplicates[str(req_file2)]
    assert "pandas" not in duplicates[str(req_file2)]

    # Check that there are no unexpected files or packages
    assert len(duplicates) == 2
    assert len(duplicates[str(req_file1)]) == 1
    assert len(duplicates[str(req_file2)]) == 1


# You might also want to add more tests for edge cases:


def test_find_duplicates_no_duplicates(tmp_path):
    req_file = tmp_path / "requirements_no_dups.txt"
    req_file.write_text("pandas==1.1.5\nnumpy==1.19.3\nmatplotlib==3.3.4")

    duplicates = find_duplicates([str(req_file)])
    assert len(duplicates) == 0


def test_find_duplicates_empty_file(tmp_path):
    req_file = tmp_path / "requirements_empty.txt"
    req_file.write_text("")

    duplicates = find_duplicates([str(req_file)])
    assert len(duplicates) == 0
