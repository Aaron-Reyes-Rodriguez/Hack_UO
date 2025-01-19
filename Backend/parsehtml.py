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

def convert_to_24_hour_start_end(time_range):
    # Split the time range into start and end times
    start_time, end_time = time_range.split(" - ")

    def to_24_hour(time):
        # parse out am/pm
        period = time[-2:].lower()
        hours, minutes = map(int, time[:-2].split(":"))

        # to 24-hour
        if period == "pm" and hours != 12:
            hours += 12
        elif period == "am" and hours == 12:
            hours = 0

        # format back to string
        return f"{hours:02}:{minutes:02}"

    # convert start and end times
    start = to_24_hour(start_time)
    end = to_24_hour(end_time)

    return start, end

def list_to_dict(course_total, times_list, days_list):
    #fix times
    start_times_list = []
    end_times_list = []
    for time in times_list:
        start_time, end_time = convert_to_24_hour_start_end(time)
        start_times_list.append(start_time)
        end_times_list.append(end_time)
    # print(start_times_list)
    # print(end_times_list)

    keys = ['Course Name', 'Day(s)', 'Start Time', 'End Time']
    num_courses = len(course_total)
    course_dict = {}
    schedule = []
    for i in range(num_courses):
        course_info = []
        course_info.append(course_total[i])
        course_info.append(days_list[i])
        course_info.append(start_times_list[i])
        course_info.append(end_times_list[i])
        course_dict = dict(zip(keys, course_info))
        schedule.append(course_dict)
    dict_to_json(schedule)

def dict_to_json(schedule_dict):
    json_string = json.dumps(schedule_dict, indent=4)
    return json_string
    #print(json_string)


#pull file name passed into function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract information from an HTML file.")
    parser.add_argument('file_path', help="The path to the HTML file")
    args = parser.parse_args()

extract_info_from_html(args.file_path)