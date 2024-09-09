import pytest
import os
import sys

from datetime import datetime

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spidercli_dir = os.path.join(project_dir, 'spider_cligen')  
sys.path.append(spidercli_dir)

from spider_cligen.utils import (
    get_or_create_file,
    get_or_create_path,
    sub_string,
    generate_mit_license,
    generate_apache_license,
    generate_project_name,
    generate_gitignore,
    generate_readme
)

# Mocks
BASE_DIR = os.path.abspath('.')
LICENSES_DIR = os.path.join(BASE_DIR, 'templates', 'licenses')

# Constants
project_owner = "MyCompany"
project_name = "MyProject"
year = datetime.now().year


# Test get_or_create_file function
def test_get_or_create_file_existing_file(tmp_path):
    # Create a temporary file
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    test_file = test_dir / "test_file.txt"
    test_file.write_text("Existing data")

    # Test if it returns the existing file path
    file_path = get_or_create_file(test_dir, "test_file.txt", "New data")
    assert file_path == str(test_file)
    assert test_file.read_text() == "Existing data"


def test_get_or_create_file_new_file(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()

    # Test if it creates a new file with the given data
    file_path = get_or_create_file(test_dir, "new_file.txt", "New data")
    assert os.path.exists(file_path)
    assert open(file_path).read() == "New data"



def test_get_or_create_path_new_path(tmp_path):
    path = get_or_create_path("new_dir", "sub_dir")
    assert os.path.exists(path)


# Test sub_string function
def test_sub_string():
    original_string = "Hello, AUTHOR/COMPANYNAME!"
    new_string = sub_string('AUTHOR/COMPANYNAME', "MyCompany", original_string)
    assert new_string == "Hello, MyCompany!"



# Test generate_project_name function
def test_generate_project_name():
    result = generate_project_name("My Project Name")
    assert result == "My_Project_Name"