# Import necessary Flask modules and os for file operations
from flask import Flask, request, send_from_directory, render_template_string
import os

# Set the directory where uploaded MP3 files will be stored
UPLOAD_FOLDER = '/usr/src/app'

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
    
    # Get list of all MP3 files in the upload directory
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.mp3')]
    
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