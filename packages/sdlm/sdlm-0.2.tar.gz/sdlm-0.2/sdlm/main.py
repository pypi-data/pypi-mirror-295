import os
import requests
from bs4 import BeautifulSoup
import re

DOWNLOAD_FOLDER = 'downloads'
DOWNLOAD_FILE = 'downloads.txt'

# Can't really test these except for rar and zips because I don't have an account
MIME_TYPE_TO_EXTENSION = {
    'application/zip': '.zip',
    'application/x-rar-compressed': '.rar',
    'application/pdf': '.pdf',
    'application/octet-stream': '',
    'text/plain': '.txt',
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'application/x-dosexec': '.exe',
    'application/x-executable': '.exe',
    'application/x-sharedlib': '.so',
    'application/x-hdf5': '.h5',
    'application/java-archive': '.jar',
    'application/vnd.android.package-archive': '.apk',
    'application/x-rar': '.rar',
    'application/vnd.microsoft.portable-executable': '.exe',
}


def get_file_extension(response):
    content_type = response.headers.get('Content-Type', '').lower()
    return MIME_TYPE_TO_EXTENSION.get(content_type, '')


def download_file(url, folder):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        extension = get_file_extension(response)
        file_name = url.split('/')[-1] + extension
        file_path = os.path.join(folder, file_name)
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0

        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
                    progress = (downloaded_size / total_size) * 100
                    progress_bar = '=' * int(progress / 2)
                    print(f"\r[{progress_bar:<50}] {progress:.2f}%", end='')

        print(f"\nDownloaded: {file_name}")
    else:
        print(f"Failed to download from {url}")


def find_download_link(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    script_tags = soup.find_all('script')

    for script in script_tags:
        if 'window.open' in script.text:
            match = re.search(r'window\.open\("([^"]+)"', script.text)
            if match:
                download_url = match.group(1)
                return download_url

    return None


def read_urls_from_file(file_path):
    urls = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    else:
        print(f"File {file_path} does not exist.")
    return urls


def main():
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    print(
        "This tool currently only supports fuckingfast.co links. If you are trying to download something from somewhere else, it might not work.")

    choice = input("Type 'read' to read URLs from downloads.txt or 'input' to enter URLs manually: ").strip().lower()

    if choice == 'read':
        urls = read_urls_from_file(DOWNLOAD_FILE)
        if not urls:
            print(f"No URLs found in {DOWNLOAD_FILE}.")
    elif choice == 'input':
        urls = []
        print("Enter the URLs (press Enter without typing anything to stop):")
        while True:
            url = input("Enter URL: ").strip()
            if not url:
                break
            urls.append(url)
    else:
        print("Invalid choice. Exiting.")
        return

    for url in urls:
        download_link = find_download_link(url)
        if download_link:
            download_file(download_link, DOWNLOAD_FOLDER)
        else:
            print(f"No download link found for {url}")


if __name__ == '__main__':
    main()
    print("Press any key to exit.")
    input()
