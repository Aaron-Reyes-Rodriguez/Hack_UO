from bs4 import BeautifulSoup
import sys
import json


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

# untested addition
# extract the class schedule
data = []
for link in soup.find_all("CLASS"):
    title = link.text.strip()  # Get the text
    href = link.get("href")   # Get the href attribute
    if href:  # Ensure the link is not None
        data.append({"title": title, "link": href})

# convert and save as JSON
json_data = json.dumps(data, indent=4)

with open("data.json", "w") as file:
    file.write(json_data)

print("Data saved to data.json")

#^--untested addition end

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract information from an HTML file.")
    parser.add_argument('file_path', help="The path to the HTML file")
    args = parser.parse_args()