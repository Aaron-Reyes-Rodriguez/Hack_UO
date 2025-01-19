from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
from Backend.parsehtml.py import extract_info_from_html
import os
from quackhacks.utils import find_common_free_times

app = Flask(__name__)

# Set up a folder for uploaded files
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'html'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'scheduleFiles' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('scheduleFiles')  # Get the list of files
    
    if not files:
        return redirect(request.url)
    
    # List to store parsed data from each HTML file
    parsed_data = []
    
    for file in files:
        #if file and allowed_file(file.filename):
            # Save the file to the upload folder
            #filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            #file.save(filename)
            # Store the result for this file
            #parsed_data.append(extract_info_from_html(filename))
        continue
    schedules = [
    [{
        "user_id": 1,
        "course": "CS 410",
        "title": "Capstone",
        "days": ["M", "W"],
        "start_time": "16:00",
        "end_time": "17:20"
    },
    {
        "user_id": 2,
        "course": "FR 203",
        "title": "2nd Year French",
        "days": ["M", "W", "F"],
        "start_time": "10:00",
        "end_time": "11:20"
    }],
    [{
        "user_id": 1,
        "course": "CS 415",
        "title": "Operating Systems",
        "days": ["M", "W"],
        "start_time": "15:00",
        "end_time": "16:20"
    },
    {
        "user_id": 2,
        "course": "MATH 343",
        "title": "Stats",
        "days": ["T", "TR", "F"],
        "start_time": "16:00",
        "end_time": "17:20"
    }]
]

# Calculate common free times using the dummy data
    common_free_times = find_common_free_times(schedules)

    #result = find_common_free_times(parsed_data)
    result = common_free_times
    # Render the result page with parsed data from all files
    return render_template('result.html', data=result)

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)