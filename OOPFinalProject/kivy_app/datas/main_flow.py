"""
main_flow.py
This module orchestrates the main data flow for searching and retrieving PC component specifications.
"""
### add new line for commit
import os
import json
from .fetch_raw_url import parse_html
from . import request_handler, web_scrape, product_parser

COMPONENT_DATA_DIR = os.path.join(os.path.dirname(__file__), 'fetch_raw_url', 'component_data')
TEMP_HTML_PATH = os.path.join(os.path.dirname(__file__), 'temp_content.html')


def get_component_url(component_type, component_name):
    """
    Find the URL for a given component type and name from the component_data JSON files.
    """
    data_file = os.path.join(COMPONENT_DATA_DIR, f"{component_type}.json")
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Component data file not found: {data_file}")
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get(component_name)


def fetch_and_parse_component(component_type, component_name):
    """
    Main flow: Given a component type and name, fetch its HTML, parse specs, and return them.
    """
    url = get_component_url(component_type, component_name)
    if not url:
        raise ValueError(f"Component '{component_name}' not found in {component_type}.json")

    # 1. Scrape HTML and save to temp_content.html
    html_content = web_scrape.scrape_website_html(url)
    with open(TEMP_HTML_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 2. Parse HTML to extract specifications
    specs = product_parser.parse_html_for_specs(html, url)
    return specs


def search_component(component_type, component_name):
    """
    Public API: Search for a component and get its specifications.
    """
    try:
        specs = fetch_and_parse_component(component_type, component_name)
        return specs
    except Exception as e:
        return {"error": str(e)}

# Example usage (for testing):
if __name__ == "__main__":
    # Example: search for a CPU
    result = search_component("cpu", "AMD A10-9700")
    print(json.dumps(result, indent=2, ensure_ascii=False))
