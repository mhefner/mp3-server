# Import necessary Flask modules and os for file operations
from flask import Flask, request, send_from_directory, render_template_string
import os

# Set the directory where uploaded MP3 files will be stored
UPLOAD_FOLDER = '/mp3-files'  # Changed from '/usr/src/app' to '/mp3-files'

# Create Flask application instance
app = Flask(__name__)
# Configure the upload folder for the Flask app
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML template for the web interface
# This creates a simple page with:
# - A list of available MP3 files (as clickable links)
# - An upload form for new MP3 files
HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>MP3 Server</title>
</head>
<body>
    <h1>MP3 Server</h1>
    <ul>
    <!-- Loop through each MP3 file and create a clickable link -->
    {% for file in files %}
        <li><a href="{{ file }}">{{ file }}</a></li>
    {% endfor %}
    </ul>
    <hr>
    <!-- File upload form that accepts only MP3 files -->
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".mp3">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
"""

# Main route that handles both displaying files and uploading new ones
@app.route('/', methods=['GET', 'POST'])
def index():
    # Handle file upload (POST request)
    if request.method == 'POST':
        # Get the uploaded file from the form
        uploaded_file = request.files.get('file')
        # Check if a file was actually uploaded
        if uploaded_file:
            # Create the full path where the file will be saved
            path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # Save the uploaded file to the server
            uploaded_file.save(path)
    
    # Debug: Check directory and files
    try:
        print(f"Looking for files in: {UPLOAD_FOLDER}")
        print(f"Directory exists: {os.path.exists(UPLOAD_FOLDER)}")
        all_files = os.listdir(UPLOAD_FOLDER)
        print(f"All files found: {all_files}")
        files = [f for f in all_files if f.endswith('.mp3')]
        print(f"MP3 files found: {files}")
        print(f"Number of MP3 files: {len(files)}")
    except Exception as e:
        print(f"Error reading directory: {e}")
        files = []
    
    # Render the HTML template with the list of MP3 files
    return render_template_string(HTML_TEMPLATE, files=files)

# Route to serve/download individual files
# The <path:filename> allows for filenames with special characters or subdirectories
@app.route('/<path:filename>')
def serve_file(filename):
    # Send the requested file from the upload directory
    # This allows users to download or stream the MP3 files
    return send_from_directory(UPLOAD_FOLDER, filename)

# Run the Flask application when this script is executed directly
if __name__ == '__main__':
    # Run on all available network interfaces (0.0.0.0) on port 8080
    # This makes the server accessible from other machines on the network
    app.run(host='0.0.0.0', port=8080)