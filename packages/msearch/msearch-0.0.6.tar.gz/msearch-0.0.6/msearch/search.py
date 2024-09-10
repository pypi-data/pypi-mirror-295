import logging
import os
import traceback

import requests
from bs4 import BeautifulSoup
from github import Github, GithubException
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)

def search_web(query: str) -> list:
    """Search the web and return results."""
    if not query.strip():
        logger.info("Please provide a search query.")
        return []

    search_url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        search_results = []
        for result in soup.select('div.g'):
            title_elem = result.select_one('h3')
            link_elem = result.select_one('a')
            snippet_elem = result.select_one('div.VwiC3b')
            
            if title_elem and link_elem and snippet_elem:
                title = title_elem.text
                url = link_elem['href']
                snippet = snippet_elem.text.strip()
                search_results.append({"title": title, "url": url, "snippet": snippet})

        return search_results
    except Exception as e:
        logger.error(f"An error occurred: {traceback.format_exc()}")
        return []

def search_github(query: str):
    """Search GitHub for repositories."""
    if not query.strip():
        return []

    github_token = os.environ.get('GITHUB_ACCESS_TOKEN')
    if not github_token:
        logger.error("GITHUB_ACCESS_TOKEN environment variable is not set.")
        raise ValueError("GITHUB_ACCESS_TOKEN environment variable is not set. Please set it to use GitHub search.")
    
    g = Github(github_token)

    try:
        max_results = 10
        results = g.search_repositories(query=query)
        
        return [
            {
                "name": repo.full_name,
                "description": repo.description,
                "url": repo.html_url,
                "stars": repo.stargazers_count,
                "forks": repo.forks_count
            }
            for repo in results[:max_results]
        ]
    except GithubException as e:
        logger.error(f"GitHub Exception: {str(e)}")
        raise RuntimeError(f"An error occurred while searching GitHub: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in search_github: {str(e)}")
        logger.exception("Exception traceback:")
        raise RuntimeError(f"An unexpected error occurred: {str(e)}")

def search_huggingface(query: str):
    """Search HuggingFace for models and datasets."""
    from huggingface_hub import HfApi

    api = HfApi()
    try:
        # Search for models
        models = api.list_models(search=query, limit=10)

        results = []
        for model in models:
            results.append({
                "name": model.modelId,
                "downloads": model.downloads,
                "likes": model.likes,
                "type": "model",
                "url": f"https://huggingface.co/{model.modelId}"
            })

        return results
    except Exception as e:
        logger.error(f"Error searching HuggingFace: {str(e)}")
        return []
    
