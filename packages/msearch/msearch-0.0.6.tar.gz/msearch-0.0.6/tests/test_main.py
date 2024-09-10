import subprocess
import sys
import pytest
import time
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def run_cli_command(command, timeout=30):
    logger.debug(f"Running CLI command: {command}")
    start_time = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "-m", "msearch.main"] + command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        logger.debug(f"Command output - stdout: {result.stdout}, stderr: {result.stderr}, returncode: {result.returncode}")
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        logger.error(f"Command '{' '.join(command)}' timed out after {timeout} seconds")
        return "", f"Command timed out after {timeout} seconds", 1
    except Exception as e:
        logger.error(f"Unexpected error during command execution: {str(e)}")
        return "", str(e), 1

def test_cli_help():
    stdout, stderr, returncode = run_cli_command(["--help"])
    assert returncode == 0
    assert "Usage:" in stdout
    assert "Options:" in stdout

@pytest.mark.parametrize("query,expected_output", [
    (["python", "cli"], "Search Results"),
    (["language:python", "stars:>1000"], "Search Results"),
])
def test_search_command(query, expected_output):
    stdout, stderr, returncode = run_cli_command(["search"] + query)
    assert returncode == 0
    assert expected_output in stdout

def test_search_command_no_results():
    stdout, stderr, returncode = run_cli_command(["search", "thisshouldnotexistatall12345"])
    assert returncode == 0
    assert "No results found" in stdout or "Search Results" in stdout

@pytest.mark.parametrize("url", [
    "https://example.com",
    "https://github.com",
])
def test_browse_command(url):
    stdout, stderr, returncode = run_cli_command(["browse", url])
    assert returncode == 0
    assert "Web Search Results" in stdout

def test_invalid_command():
    stdout, stderr, returncode = run_cli_command(["invalid-command"])
    assert returncode == 0
    assert "Usage:" in stdout or "Error:" in stderr

def test_web_search():
    stdout, stderr, returncode = run_cli_command(["search", "web", "python programming"])
    assert returncode == 0
    assert "Web Search Results" in stdout

def test_github_search():
    stdout, stderr, returncode = run_cli_command(["search", "--engine", "github", "python"])
    assert returncode == 0
    assert "GitHub Search Results" in stdout

def test_pypi_search():
    stdout, stderr, returncode = run_cli_command(["search", "--engine", "pypi", "requests"])
    assert returncode == 0
    assert "PyPI Search Results" in stdout

def test_huggingface_search():
    stdout, stderr, returncode = run_cli_command(["search", "--engine", "hf", "bert"])
    assert returncode == 0
    assert "HuggingFace Search Results" in stdout

def test_minspect_usage():
    stdout, stderr, returncode = run_cli_command(["--engine", "inspect", "os"])
    assert returncode == 0
    assert "Module Inspection" in stdout
    assert "Inspecting module: os" in stdout
