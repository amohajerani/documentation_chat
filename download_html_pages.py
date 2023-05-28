import requests
import os
from urllib.parse import urlparse, urljoin

def download_page(url):
    response = requests.get(url)
    return response.content

def save_page(content, path):
    with open(path, 'wb') as f:
        f.write(content)

def download_website(url, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize URL-to-file mapping dictionary
    url_to_file = {}

    # Download the initial page
    homepage_content = download_page(url)
    homepage_file = 'index.html'
    save_page(homepage_content, os.path.join(output_dir, homepage_file))
    url_to_file[url] = homepage_file

    # Parse the homepage to extract links
    parsed_url = urlparse(url)
    base_url = parsed_url.scheme + '://' + parsed_url.netloc
    links = extract_links(homepage_content, base_url)
    import pdb; pdb.set_trace()
    # Download linked pages recursively
    for link in links:
        absolute_url = urljoin(base_url, link)
        page_content = download_page(absolute_url)
        filename = get_filename_from_url(link)
        save_page(page_content, os.path.join(output_dir, filename))
        url_to_file[absolute_url] = filename

    return url_to_file

def extract_links(html, base_url):
    # Use a HTML parser library like BeautifulSoup to extract links
    # Here's an example using BeautifulSoup:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, 'html.parser')
    links = []

    for anchor in soup.find_all('a'):
        href = anchor.get('href')
        if href:
            absolute_url = urljoin(base_url, href)
            links.append(absolute_url)

    return links

def get_filename_from_url(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    if not filename or filename == '/':
        filename = 'index.html'
    return filename

# Example usage
website_url = 'https://docs.synapsefi.com'
output_directory = 'downloaded_website'

#url_to_file_mapping = download_website(website_url, output_directory)
#for url, file_name in url_to_file_mapping.items():
#    print(f"URL: {url}\tFile: {file_name}")

