import asyncio
import html
import inspect
import logging
import re
import time
import traceback
from typing import Any, Callable

import click
from mbpy.mpip import find_and_sort
from minspect.inspecting import inspect_library
from mrender.md import Markdown
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme

from msearch.browse import browse
from msearch.parse import mparse
from msearch.search import search_github, search_huggingface, search_web

custom_theme = Theme({"default": "on white"})
console = Console(theme=custom_theme)
logger = logging.getLogger(__name__)

def parse_and_run(query: str, func: Callable) -> Any:
    args, kwargs = mparse(query)
    for key, value in kwargs.items():
        value: str = str(value)
        if value.isnumeric():
            kwargs[key] = float(value)
        elif value.lower() in ['true', 'false']:
            kwargs[key] = value.lower() == 'true'
    try:
        return func(*args, **kwargs)
    except Exception as e:
        console.print(Panel(f"Error: {e}", title="Error", style="bold red"))
        console.print(f"Received args: {args} and kwargs: {kwargs}")
        console.print(Panel(f"Correct usage: {inspect.signature(func)}", title="Usage"))
        exit(1)



def handle_inspect_query(query):
    if "depth" not in query:
        query += " depth=0"
    if "signatures" not in query:
        query += " signatures=True"
    if "docs" not in query:
        query += " docs=False"
    result = parse_and_run(query, inspect_library)
    console.print(Panel(f"Inspecting module: {query}", title="Module Inspection"))
    console.print(Panel(result.get('functions', 'No functions found'), title="Functions"))
    console.print(Panel(result.get('classes', 'No classes found'), title="Classes"))
    console.print(Panel(result.get('variables', 'No variables found'), title="Variables"))
    return result

def handle_pypi_query(query):
    result = parse_and_run(query, find_and_sort)
    display_pypi_results(result)

def handle_huggingface_query(query):
    result = parse_and_run(query, search_huggingface)
    if not result:
        console.print(Panel("No results found.", title="HuggingFace Search"))
    else:
        display_huggingface_results(result)


search_functions = {
        'web': search_web,
        'github': search_github,
        'inspect': handle_inspect_query,
        'pypi': handle_pypi_query,
        'hf': handle_huggingface_query
    }
    

def run_search(query: str, engine: str, interactive: bool):

    results = search_functions[engine](query)
    
    if not results:
        console.print(Panel(f"No results found.", title=f"{engine.capitalize()} Search Results"))
    else:
        results = display_results(results, engine)
        interact_display = handle_interactive_mode(results, engine, interactive=interactive)
        if not interactive:
            return interact_display
    return results

@click.command()
@click.argument('query', nargs=-1)
@click.option('--engine', '-e', default='web', help='Search engine to use: web, github, inspect, pypi, hf')
@click.option('--interactive', '-i', is_flag=True, default=False, help='Enable interactive mode')
def cli(query, engine: str, interactive: bool):
    """Search for info on the web, github, pypi, or inspect a library."""
    query = ' '.join(query)
 
    if engine not in search_functions:
        console.print(f"Invalid search engine: {engine}")
        return 1
    
    return run_search(query, engine, interactive)
    

def display_results(results, engine):
    if engine == 'web':
        display_web_results(results)
    elif engine == 'github':
        display_github_results(results)
    elif engine == 'pypi':
        display_pypi_results(results)
    elif engine == 'hf':
        display_huggingface_results(results)
    else:
        console.print(f"Display not implemented for {engine} results.")
    return results

def display_web_results(results):
    table = Table(title="Web Search Results", show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Index", style="cyan", width=10)
    table.add_column("Title", style="cyan", width=40, overflow="fold")
    table.add_column("URL", style="blue", width=40, no_wrap=True)
    table.add_column("Snippet", style="green", width=40, overflow="fold")
    for i, result in enumerate(results, 1):
        table.add_row(
            str(i),
            result.get('title', 'No title'),
            result.get('url', 'No URL'),
            result.get('snippet', 'No snippet')
        )
    console.print(Panel(table, expand=True))
    return result

def handle_interactive_mode(results, engine, interactive=False):
    choice = 0 if not interactive else -1
    while choice != 'q':
        options = [f"{i}. {result.get('url', result.get('title', 'No title'))}" for i, result in enumerate(results, 1)]
        options.append("q. Quit")
        for option in options:
            console.print(option)
        choice = 0 if not interactive else Prompt.ask("Choose an option", choices=[str(i) for i in range(1, len(results) + 1)] + ['q'])
        
        if interactive and choice.lower() == 'q':
            break
        
        index = int(choice) - 1
        result = results[index]
        results = ""
        if engine == 'web':
            display_web_content(result, interactive=interactive)
        elif engine == 'github':
            display_github_content(result)
        elif engine == 'pypi':
            display_pypi_content(result)
        elif engine == 'hf':
             display_huggingface_content(result)
        else:
            console.print(f"Content display not implemented for {engine} results.")
        
        if not interactive:
            return results
    return results




def clean(content):
    """Clean web content by removing non-legible text, ensuring headers are on new lines, preserving comments, and handling code blocks."""
    # Define a regular expression pattern to match CSS blocks and data-styled attributes
    css_pattern = re.compile(r'data-styled\.[a-zA-Z0-9_-]+\[id="[^"]+"\]\{content:"[^"]+"\}/!sc/|'
                             r'\.[a-zA-Z0-9_-]+\{[^}]*\}/!sc/')
    if not isinstance(content, str):
        if hasattr(content, '__iter__'):
            return [clean(item) for item in content]
        return content
    if isinstance(content, dict):
        return {k: clean(v) for k, v in content.items()}
    # Remove CSS blocks using the pattern
    cleaned_content = re.sub(css_pattern, '', content)

    # Remove inline styles and script tags
    cleaned_content = re.sub(r'<style[^>]*>.*?</style>', '', cleaned_content, flags=re.DOTALL)
    cleaned_content = re.sub(r'<script[^>]*>.*?</script>', '', cleaned_content, flags=re.DOTALL)

    # Remove HTML tags
    cleaned_content = re.sub(r'<[^>]+>', '', cleaned_content)

    # Ensure headers are on new lines and preserve the newline after them
    cleaned_content = re.sub(r'(?m)^\s*(#+\s.*?)(\s*\[.*?\]\(.*?\))?\s*$', r'\n\1\2\n', cleaned_content)

    # Preserve comments by ensuring they are not treated as headers
    cleaned_content = re.sub(r'(?<!\n)(#(?!#).*)', r'\n\1', cleaned_content)

    # Handle code blocks by ensuring they are preserved with surrounding newlines
    code_block_pattern = re.compile(r'```.*?```', re.DOTALL)
    cleaned_content = re.sub(code_block_pattern, lambda match: f"\n{match.group(0)}\n", cleaned_content)

    # Handle inline code by ensuring it is surrounded by backticks
    cleaned_content = re.sub(r'`([^`]+)`', r'`\1`', cleaned_content)

    # Remove excessive whitespace while preserving necessary newlines
    cleaned_content = re.sub(r' {2,}', ' ', cleaned_content)
    cleaned_content = re.sub(r'\n{3,}', '\n\n', cleaned_content)

    return cleaned_content.strip()

def display_web_content(result, interactive=False):
    old_result = result.copy()
    console.print(f"Title: {result['title']}", style="cyan")
    console.print(f"URL: {result['url']}", style="blue")
    content = browse([result['url']], interactive=interactive)[0]
    content = content.get('content')
    if not content:
        console.print("No content found.", style="bold red")
        return
    console.print(f"Title: {result['title']}", style="cyan")
    console.print("Content:", style="yellow")
    print(content)
    md = Markdown(content)

    words = md.lines
    total_words = len(words)
    current_position = 0


    while current_position < total_words:
        chunk = words[current_position:current_position + 500]
        Markdown(chunk).stream()
        current_position += 2000
        
        if current_position < total_words:  # noqa: SIM102
            if interactive and Prompt.ask("Continue reading?", choices=["y", "n"], default="y") != "y":

                return None

    return old_result
# def display_web_content(result):
#     url = result['url']
#     browse_result = browse([url], interactive=True)[0]
    
#     if 'error' in browse_result:
#         console.print(f"Error for {url}: {browse_result['error']}", style="bold red")
#     else:
#         console.print(f"Title: {browse_result['title']}", style="cyan")
#         console.print("Content:", style="yellow")
#         console.print(Markdown(browse_result['content']))

def display_github_content(result):
    console.print(f"Repository: {result['name']}", style="cyan")
    console.print(f"URL: {result['url']}", style="blue")
    console.print(f"Description: {result['description']}", style="green")
    console.print(f"Stars: {result['stars']}", style="yellow")
    console.print(f"Forks: {result['forks']}", style="yellow")

def display_pypi_content(result):
    console.print(f"Package: {result['name']}", style="cyan")
    console.print(f"Version: {result['version']}", style="magenta")
    console.print(f"Description: {result['summary']}", style="green")

def display_huggingface_content(result):
    console.print(f"Name: {result['name']}", style="cyan")
    console.print(f"Type: {result['type'].capitalize()}", style="magenta")
    console.print(f"URL: {result['url']}", style="blue")
    console.print(f"Downloads: {result['downloads']}", style="green")
    console.print(f"Likes: {result['likes']}", style="yellow")

def display_github_results(results):
    table = Table(title="GitHub Search Results")
    table.add_column("Repository", style="cyan", no_wrap=True)
    table.add_column("URL", style="magenta")
    table.add_column("Description", style="green")
    table.add_column("Stars", justify="right", style="yellow")
    table.add_column("Forks", justify="right", style="yellow")
    for repo in results:
        table.add_row(repo['name'], repo['url'], repo['description'], str(repo['stars']), str(repo['forks']))
    console.print(Panel(table))

def display_pypi_results(results):
    table = Table(title="PyPI Search Results")
    table.add_column("Package", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Description", style="green")
    for package in results:
        table.add_row(package['name'], package['version'], package['summary'])
    console.print(Panel(table))

def display_huggingface_results(results):
    table = Table(title="HuggingFace Search Results", show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("URL", style="blue")
    table.add_column("Downloads", justify="right", style="green")
    table.add_column("Likes", justify="right", style="yellow")
    for item in results:
        table.add_row(item['type'].capitalize(), item['name'], item['url'], str(item['downloads']), str(item['likes']))
    console.print(Panel(table, expand=False))
    console.print(Panel(f"Total results: {len(results)}", title="Summary", style="bold green"))

if __name__ == "__main__":
    exit(cli())
