import pytest
from interrogate import coverage
import subprocess
import os
import numpy
from zot2sioyek.zot2sioyek import check_env_variables

@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    doctest_namespace["np"] = numpy

pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    check_env_variables()
    tests_path = os.path.abspath(os.getcwd())
    file_to_check = tests_path + "/src/zot2sioyek/zot2sioyek.py"
    result = subprocess.run(
        [
            "interrogate",
            file_to_check
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        pytest.exit("Interrogate command failed", returncode=result.returncode)
