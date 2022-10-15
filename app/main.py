from flask import Flask, request, redirect, jsonify, render_template, send_from_directory, url_for
import os
from app.torch_utils import test

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files'

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        if request.files:
            pdf = request.files["pdf"]
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename))
            test()
            return send_from_directory(app.config['UPLOAD_FOLDER'], pdf.filename, as_attachment=True)
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'result':1})

