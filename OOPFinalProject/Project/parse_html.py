import os
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
# The path to the HTML file you want to parse.
HTML_FILE_PATH = 'page_source.html'
# The base URL of the website to construct full product URLs.
BASE_URL = 'https://pcpartpicker.com'

def parse_product_urls_from_file(file_path: str):
    """
    Reads and parses a single HTML file to extract all product URLs.

    Args:
        file_path (str): The full path to the HTML file.

    Returns:
        list[str] or None: A list of full product URLs, or None if the file is not found.
    """
    # 1. Validate if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found at '{file_path}'.")
        return None

    print(f"--- Starting to parse file: {file_path} ---")
    
    # 2. Read the HTML content from the file
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    # 3. Create a BeautifulSoup object for parsing
    # 'lxml' is a fast and efficient parser
    soup = BeautifulSoup(html_content, 'lxml')
    
    # 4. Find all anchor tags (<a>) containing the product links
    # The correct CSS selector is "td.td__name > a"
    product_link_tags = soup.select("td.td__name > a")
    
    if not product_link_tags:
        print(f"Warning: No product links found using the selector 'td.td__name > a' in {file_path}.")
        return []
        
    print(f"Found {len(product_link_tags)} product links in the file.")
    
    # 5. Extract the 'href' attribute from each tag
    all_product_urls = []
    for tag in product_link_tags:
        # Use .get('href') to safely get the attribute, avoiding errors
        relative_url = tag.get('href')
        
        if relative_url:
            # Construct the absolute URL
            full_url = BASE_URL + relative_url
            all_product_urls.append(full_url)
            
    return all_product_urls

# --- Main execution block ---
if __name__ == "__main__":
    # Call the parsing function
    extracted_urls = parse_product_urls_from_file(HTML_FILE_PATH)
    
    print("\n--- PARSING COMPLETE ---")
    
    # Display and save the results
    if extracted_urls is not None: # Check for None in case of file not found
        if extracted_urls: # Check if the list is not empty
            print(f"Successfully extracted {len(extracted_urls)} URLs.")
            
            # Print the first 10 URLs for a quick preview
            print("\nFirst 10 URLs found:")
            for url in extracted_urls[:10]:
                print(f"- {url}")
            
            # (Optional) Save the list of URLs to a .txt file
            output_filename = "product_urls.txt"
            with open(output_filename, 'w', encoding='utf-8') as f:
                for url in extracted_urls:
                    f.write(url + '\n')
            print(f"\nAll URLs have been saved to '{output_filename}'.")
            
        else: # Case where the list is empty
            print("No product URLs were found in the file.")
    else: # Case where the function returned None
        print("Process failed. Please check the file path.")