import os
import pytest
import sys
from unittest import mock
from datetime import datetime, timezone, timedelta

# Add the directory containing chkexemp to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chkexmpt.main import (parse_blame_output, run_grep, run_git_blame, get_threshold_date, list_files, load_config, run_reporting)

def test_parse_blame_output():
    blame_output = "abc12345 (John Doe 2023-09-09 12:34:56 +0000 1) some code"
    blame_pattern = r"(\w{8}) \((.*?) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [-+]\d{4})"
    git_hash, author, timestamp = parse_blame_output(blame_output, blame_pattern)
    
    assert git_hash == "abc12345"
    assert author == "John Doe"
    assert timestamp == datetime(2023, 9, 9, 12, 34, 56, tzinfo=timezone.utc)

def test_parse_blame_output_no_match():
    blame_output = "no match here"
    blame_pattern = r"(\w{8}) \((.*?) (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} [-+]\d{4})"
    git_hash, author, timestamp = parse_blame_output(blame_output, blame_pattern)
    
    assert git_hash is None
    assert author is None
    assert timestamp is None

@mock.patch("subprocess.run")
def test_run_grep(mock_subprocess_run):
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = "1:match1\n2:match2"
    
    returncode, output = run_grep("pattern", "file.txt")
    
    assert returncode == 0
    assert output == ["1:match1", "2:match2"]

@mock.patch("subprocess.run")
def test_run_git_blame(mock_subprocess_run):
    mock_subprocess_run.return_value.returncode = 0
    mock_subprocess_run.return_value.stdout = "blame output"
    
    returncode, output = run_git_blame(1, "file.txt")
    
    assert returncode == 0
    assert output == "blame output"

def test_get_threshold_date():
    allowed_days = 30
    current_time = datetime.now()
    blame_timestamp = current_time - timedelta(days=23)
    threshold_date = get_threshold_date(blame_timestamp, allowed_days)

    assert threshold_date < blame_timestamp

@mock.patch("os.walk")
def test_list_files(mock_os_walk):
    mock_os_walk.return_value = [
        ("/some/path", ["dir1"], ["file1.tf", "file2.py"]),
        ("/some/path/dir1", [], ["file3.tf"]),
    ]
    
    file_patterns = ["*.tf"]
    directory_path = "/some/path"
    ignore_paths = [".terraform"]
    
    files = list_files(file_patterns, directory_path, ignore_paths)
    
    assert files == sorted(["/some/path/file1.tf", "/some/path/dir1/file3.tf"])

@mock.patch("builtins.open", new_callable=mock.mock_open, read_data="allowed_days: 10")
@mock.patch("os.path.exists", return_value=True)
def test_load_config(mock_exists, mock_open):
    config = load_config(".chkexmp.yaml")
    
    assert config["allowed_days"] == 10
    assert config["ignore_paths"] == [".terraform"]

def test_run_reporting_dryrun():
    results = {"result1", "result2"}
    dryrun = True
    
    with mock.patch("sys.exit") as mock_exit:
        run_reporting(results, dryrun)
        mock_exit.assert_not_called()

def test_run_reporting_exit():
    results = {"result1", "result2"}
    dryrun = False
    
    with mock.patch("sys.exit") as mock_exit:
        run_reporting(results, dryrun)
        mock_exit.assert_called_once_with(1)

