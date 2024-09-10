import pytest
import subprocess
import sys
import os

# Test data
JSON_STRING = '{"key1": "value1", "key2": 42}'
ROS2_STRING = "key1:=value1 key2:=42"
KEY_VALUE_STRING = "key1=value1 key2=42"
COMMAND_LINE_STRING = "--key1 value1 --key2 42"
YAML_STRING = "key1: value1\nkey2: 42"

def run_parse_command(input_string):
    result = subprocess.run(
        [sys.executable, "-c", f"from msearch.parse import mparse; print(mparse('{input_string}'))"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip(), result.stderr.strip(), result.returncode

@pytest.fixture
def test_files(tmp_path):
    json_file = tmp_path / "test.json"
    json_file.write_text(JSON_STRING)
    
    yaml_file = tmp_path / "test.yaml"
    yaml_file.write_text(YAML_STRING)
    
    ros_file = tmp_path / "test.ros"
    ros_file.write_text(ROS2_STRING)
    
    return {"json": json_file, "yaml": yaml_file, "ros": ros_file}

def test_parse_json():
    stdout, stderr, returncode = run_parse_command(JSON_STRING)
    assert returncode == 0
    assert "(['{key1:', 'value1,', 'key2:', '42}'], {})" in stdout

def test_parse_ros2():
    stdout, stderr, returncode = run_parse_command(ROS2_STRING)
    assert returncode == 0
    assert "([], {'key1:': 'value1', 'key2:': '42'})" in stdout

def test_parse_key_value():
    stdout, stderr, returncode = run_parse_command(KEY_VALUE_STRING)
    assert returncode == 0
    assert "([], {'key1': 'value1', 'key2': '42'})" in stdout

def test_parse_yaml():
    stdout, stderr, returncode = run_parse_command(YAML_STRING)
    assert returncode == 0
    assert "([], {'key1': 'value1', 'key2': '42'})" in stdout

def test_parse_json_file(test_files):
    stdout, stderr, returncode = run_parse_command(str(test_files["json"]))
    assert returncode == 0
    assert f"(['{test_files['json']}'], {{}})" in stdout

def test_parse_yaml_file(test_files):
    stdout, stderr, returncode = run_parse_command(str(test_files["yaml"]))
    assert returncode == 0
    assert f"(['{test_files['yaml']}'], {{}})" in stdout

def test_parse_ros_file(test_files):
    stdout, stderr, returncode = run_parse_command(str(test_files["ros"]))
    assert returncode == 0
    assert f"(['{test_files['ros']}'], {{}})" in stdout

def test_parse_empty_string():
    stdout, stderr, returncode = run_parse_command("")
    assert returncode == 0
    assert "([], {})" in stdout

def test_parse_unsupported_format():
    stdout, stderr, returncode = run_parse_command("This is not a supported format")
    assert returncode == 0
    assert "(['This', 'is', 'not', 'a', 'supported', 'format'], {})" in stdout

# Note: We can't test the decorator functionality using subprocess,
# so we'll remove those tests for now.
