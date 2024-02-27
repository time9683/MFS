import pytest
from shell import Shell

# Initializing shell to test methods
shell = Shell()
shell.load()

def test_valid_path():
    assert shell.valid_path("C:/Folder1") == True
    assert shell.valid_path("C:Folder1") == False
    assert shell.valid_path("C:/F") == False