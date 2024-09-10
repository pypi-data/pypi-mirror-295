import logging as log
import re
import urllib.parse

import requests
from bs4 import BeautifulSoup
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Span, Text
import json

console = Console(style="bold white on cyan1", soft_wrap=True)
blue_console = Console(style="bold white on blue", soft_wrap=True)
print = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="red", overflow="fold")) for arg in args), **kwargs) # noqa
print_bold = lambda *args, **kwargs: console.print(*(Panel(Text(str(arg),style="bold", overflow="fold")) for arg in args), **kwargs)
input = lambda arg, **kwargs: Confirm.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, default="y", **kwargs) # noqa
ask = lambda arg, **kwargs: Prompt.ask(Text(str(arg), spans=[Span(0, 100, "blue")]), console=blue_console, **kwargs) # noqa

def is_valid_url(url) -> bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


def html_to_json(soup, base_url=None):
    """Convert HTML content to nested JSON format."""
    json_data = []

    for element in soup.descendants:
        # Skip elements inside <style> tags
        if element.parent.name == 'style':
            continue
  
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            json_data.append({f"\n{'#' * min(1, level-1)} {element.get_text(strip=True)}": ""})
        elif element.name == 'p':
            for string in element.get_text().split('\n'):
                if string.startswith("`") or string.startswith("```") or string.endswith("`") or string.endswith("```"):
                    json_data.append({"type": "python", "content": string.removeprefix("`").removesuffix("`")})
                else:
                    json_data.append({"": string})
        elif element.name == 'pre':
            code = element.find('code')
            if code:
                json_data.append({"type": "python", "content": code.get_text()})
        elif element.name == 'ul':
            ul_data = []
            for li in element.find_all('li'):
                ul_data.append(li.get_text(strip=True))
            json_data.append({"": "\n".join(f"{item}" if not item.strip().startswith('-') and not item.strip().startswith('*') and not item.strip().startswith('#')\
                and not item.strip().startswith('1.') and not item.strip().startswith('`)') and not item.strip().startswith('```')\
                 else item for item in ul_data)})  
        elif element.name == 'ol':
            ol_data = []
            for i, li in enumerate(element.find_all('li'), 1):
                ol_data.append({f"{i}.": li.get_text(strip=True)})
            json_data.append({"ordered_list": ol_data})
        elif element.name == 'a':
            href = element.get('href', '')
            text = element.get_text(strip=True)
            json_data.append({"": f"[{text}]({urllib.parse.urljoin(base_url, href)})"})
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', '')
            json_data.append({"": f"![{alt}]({urllib.parse.urljoin(base_url, src)})"})

    return json_data

def browse(urls, timeout=25, interactive=False):
    log.debug(f"browse function called with urls: {urls}, timeout: {timeout}, interactive: {interactive}")
    results = []
    for i, url in enumerate(urls):
        try:
            log.debug(f"Sending GET request to {url}")
            response = requests.get(url, timeout=timeout)
            log.debug(f"Response status code: {response.status_code}")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html5lib')

            title = soup.title.string if soup.title else "No title found"
            
            # Extract the main content
            main_content = soup.find('div', class_='markdown-body')
            if not main_content:
                main_content = soup.find('div', id='readme')
            if not main_content:
                main_content = soup.find('article')
            if not main_content:
                main_content = soup.find('main')
            if not main_content:
                main_content = soup.body

            markdown_content = html_to_json(main_content, base_url=url)
            # log.debug(f"Main content HTML: {main_content.prettify()[:200]}...")  # Log the first 200 characters of the main content HTML
            # log.debug(f"Markdown content: {markdown_content[:200]}...")  # Log the first 200 characters for debugging
            
            # Clean up the markdown content
            # markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)  # Remove excessive newlines
            # markdown_content = re.sub(r'^\s+|\s+$', '', markdown_content, flags=re.MULTILINE)  # Trim leading/trailing whitespace
            
            result = {
                'url': url,
                'title': title,
                'content': markdown_content,
            }
            results.append(result)
            
            log.info(f"Processed: {url}")
        except requests.exceptions.RequestException as e:
            log.error(f"Error fetching the webpage {url}: {str(e)}")
            error_message = f"Error fetching the webpage: {e.response.status_code if hasattr(e, 'response') else str(e)}"
            results.append({
                'url': url,
                'error': error_message,
            })
        except Exception as e:
            log.error(f"Unexpected error while browsing {url}: {str(e)}")
            log.exception("Exception traceback:")
            results.append({
                'url': url,
                'error': f"Error browsing {url}: {str(e)}",
            })
    
    return results

if __name__ == "__main__":
    # Example usage
    pass
