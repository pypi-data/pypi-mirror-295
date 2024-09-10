import pytest
from msearch.search import search_web, search_github, search_huggingface
from msearch.browse import is_valid_url, browse

def test_search_web():
    results = search_web("Python programming")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, dict) for result in results)
    assert all('title' in result and 'url' in result and 'snippet' in result for result in results)

def test_search_github():
    results = search_github("Python web framework")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, dict) for result in results)

def test_search_huggingface():
    results = search_huggingface("text classification")
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(result, dict) for result in results)

def test_is_valid_url():
    assert is_valid_url("https://www.example.com")
    assert not is_valid_url("not a url")

@pytest.mark.asyncio
async def test_browse():
    urls = ["https://www.example.com", "https://www.python.org"]
    results = await browse(urls, interactive=False)
    assert isinstance(results, list)
    assert len(results) == len(urls)
    for result in results:
        assert isinstance(result, dict)
        assert 'url' in result
        assert 'title' in result or 'error' in result
        if 'error' not in result:
            assert 'content' in result
            assert 'links' in result
