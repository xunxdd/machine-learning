from app import app
import os
from flask import request, jsonify
from flask import render_template
from werkzeug.utils import secure_filename
from app.dog_classifier import get_label

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)
            breed = get_label(img_path)
            return jsonify({'file': filename, 'breed': breed})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug=True)