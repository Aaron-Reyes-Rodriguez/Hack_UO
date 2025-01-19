from flask import Flask, render_template, request, redirect, url_for
from bs4 import BeautifulSoup
import os

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
        if file and allowed_file(file.filename):
            # Save the file to the upload folder
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)


            # Open and parse the uploaded HTML file
            with open(filename, 'r') as f:
                html_content = f.read()
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Example: Extract all <h1> tags from the HTML
            headers = soup.find_all('h1')
            header_text = [header.text for header in headers]

            # Store the result for this file
            parsed_data.append({
                'filename': file.filename,
                'headers': header_text
            })
        else:
            # If a file is invalid
            parsed_data.append({
                'filename': file.filename,
                'headers': 'Invalid file format!'
            })

    # Render the result page with parsed data from all files
    return render_template('result.html', parsed_data=parsed_data)

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)