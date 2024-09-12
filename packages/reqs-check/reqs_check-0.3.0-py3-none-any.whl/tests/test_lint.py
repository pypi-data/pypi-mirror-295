from reqs_check.lint import lint_requirements
import logging


def test_lint_requirements(tmp_path):
    req_file = tmp_path / "requirements.txt"
    req_file.write_text(
        "pandas>=1.1.5\nnumpy\nscipy~=1.5.4\n-e git+https://github.com/user/repo.git#egg=package"
    )

    warnings = lint_requirements(req_file)
    logging.debug(warnings)

    assert len(warnings) == 3
    assert "does not specify a version" in warnings[0]
    assert "uses editable installs" in warnings[2]
