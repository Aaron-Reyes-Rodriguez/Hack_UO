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
    target_table = soup.find_all("table", class_="datadisplaytable")

    child_ctr = 0
    for child in target_table[1].children: #tr tags
        child_ctr += 1
    
    #getting the info into lists
    course_nums_list = []
    course_names_list = []
    days_list = []
    times_list = []
    index_ctr = 0
    for child in target_table[1].children:
        index_ctr += 1
        if index_ctr in range(4, child_ctr - 1, 2):
            grandchildren = child.find_all("td")
            for num in grandchildren[1]:
                course_nums_list.append(num)
            for name in grandchildren[2]:
                course_names_list.append(name)
            for day in grandchildren[8]:
                days_list.append(day)
            for time in grandchildren[9]:
                times_list.append(time)
    course_total = [' '.join(z) for z in zip(course_nums_list, course_names_list)]
    list_to_dict(course_total, times_list, days_list)

def list_to_dict(course_total, times_list, days_list):
    #fix times
    start_times_list = []
    end_times_list = []
    #for str in times_list:
    #    tempstart = str.

    keys = ['Course Name', 'Day(s)', 'Time']
    num_courses = len(course_total)
    course_dict = {}
    schedule = []
    for i in range(num_courses):
        course_info = []
        course_info.append(course_total[i])
        course_info.append(days_list[i])
        course_info.append(times_list[i])
        course_dict = dict(zip(keys, course_info))
        schedule.append(course_dict)
    print(times_list)


# untested addition
# extract the class schedule
# data = []
# for link in soup.find_all("CLASS"):
#     course = link.text.strip()  # Get the text
#     href = link.get("href")   # Get the href attribute
#     if href:  # Ensure the link is not None
#         data.append({"course": course, "link": href})

# convert and save as JSON
# json_data = json.dumps(data, indent=4)

# with open("data.json", "w") as file:
#     file.write(json_data)

# print("Data saved to data.json")

#^--untested addition end

#pull file name passed into function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract information from an HTML file.")
    parser.add_argument('file_path', help="The path to the HTML file")
    args = parser.parse_args()

extract_info_from_html(args.file_path)