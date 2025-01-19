from bs4 import BeautifulSoup
import sys
import json

import argparse

def extract_info_from_html(file_path):
    try:
        #if not an .html file
        if not file_path.lower().endswith('.html'):
            raise ValueError("Error: The provided file is not an HTML file.")
        
        # Open and read the HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        save_class_info(soup)

    #if file is not found
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")

def save_class_info(soup):
    td_tags = soup.find_all('td')
    class1_name = td_tags[30].get_text() 
    class1_git  = td_tags[37]

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

#pull file name passed into function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract information from an HTML file.")
    parser.add_argument('file_path', help="The path to the HTML file")
    args = parser.parse_args()

extract_info_from_html(args.file_path)
