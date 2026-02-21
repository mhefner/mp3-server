from flask import Flask, request, send_from_directory, render_template
import os

UPLOAD_FOLDER = '/mp3-files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_categories():
    try:
        return sorted([d for d in os.listdir(UPLOAD_FOLDER)
                       if os.path.isdir(os.path.join(UPLOAD_FOLDER, d))])
    except Exception:
        return []


def get_files(category=None):
    results = []
    base = UPLOAD_FOLDER
    if category:
        dirs = [category]
    else:
        dirs = get_categories()

    for d in dirs:
        folder = os.path.join(base, d)
        try:
            for f in sorted(os.listdir(folder)):
                if f.lower().endswith('.mp3'):
                    results.append({"name": f, "category": d, "path": f"{d}/{f}"})
        except Exception:
            pass

    if not category:
        try:
            for f in sorted(os.listdir(base)):
                if f.lower().endswith('.mp3') and os.path.isfile(os.path.join(base, f)):
                    results.append({"name": f, "category": None, "path": f})
        except Exception:
            pass

    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files.get('file')
        category = request.form.get('category', '').strip()
        if uploaded_file and uploaded_file.filename:
            if category:
                dest = os.path.join(UPLOAD_FOLDER, category)
                os.makedirs(dest, exist_ok=True)
            else:
                dest = UPLOAD_FOLDER
            uploaded_file.save(os.path.join(dest, uploaded_file.filename))

    selected = request.args.get('category', '')
    categories = get_categories()
    files = get_files(selected if selected else None)
    return render_template('index.html', categories=categories, files=files, selected=selected)


@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
