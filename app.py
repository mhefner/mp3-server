from flask import Flask, request, send_from_directory, render_template_string
import os

UPLOAD_FOLDER = '/usr/src/app'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>MP3 Server</title>
</head>
<body>
  <h1>MP3 Server</h1>
  <ul>
    {% for file in files %}
      <li><a href="{{ file }}">{{ file }}</a></li>
    {% endfor %}
  </ul>
  <hr>
  <form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" accept=".mp3">
    <input type="submit" value="Upload">
  </form>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        if uploaded_file:
            path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(path)
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.mp3')]
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
