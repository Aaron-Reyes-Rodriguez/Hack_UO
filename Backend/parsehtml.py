from bs4 import BeautifulSoup
import sys

def extract_info_from_html(file_path):
    try:
        # Open and read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")

    print(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract information from an HTML file.")
    parser.add_argument('file_path', help="The path to the HTML file")
    args = parser.parse_args()