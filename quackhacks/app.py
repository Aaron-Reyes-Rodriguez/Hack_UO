from flask import Flask, render_template, request, redirect, url_for
# from bs4 import BeautifulSoup

from parsehtml import extract_info_from_html
import os
from utils import find_common_free_times

app = Flask(__name__)

# Set up a folder for uploaded file

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
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            file.save(file.filename)
            # Store the result for this file
            parsed_data.append(extract_info_from_html(file.filename))
# Calculate common free times using the dummy data
    result = find_common_free_times(parsed_data)
    print(result)
    # Render the result page with parsed data from all files
    return render_template('result.html', data=result)

if __name__ == '__main__':
    app.run(debug=True)