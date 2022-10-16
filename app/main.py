import csv
from lib2to3.pgen2 import token
from flask import Flask, request, redirect, jsonify, render_template, send_from_directory, url_for
import os
from app.torch_utils import SummarizeParagraph
from transformers import BertForSequenceClassification
from transformers import BertTokenizer
import requests

def load_model():
    model = BertForSequenceClassification.from_pretrained(
        "bert-base-uncased",
        num_labels = 2,      
        output_attentions = False,
        output_hidden_states = False,
    )
    return model

def load_tokenizer():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)
    return tokenizer


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files/'
app.config['DOWNLOAD_FOLDER'] = 'download_files/'
model=load_model()
model_trained = model.from_pretrained("saved_model")
tokenizer=load_tokenizer()
tokenizer_trained = tokenizer.from_pretrained("saved_model")

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == "POST":
        if request.files:
            pdf = request.files["pdf"]
            pdf.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename))
            csv_name=pdf.filename.replace('pdf', 'csv')
            summarize=SummarizeParagraph(pdf_name=pdf.filename, 
                                         upload_folder=app.config['UPLOAD_FOLDER'], 
                                         model=model, 
                                         tokenizer=tokenizer)
            risk_df=summarize.run()
            risk_df.to_csv(app.config['DOWNLOAD_FOLDER']+csv_name)
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], csv_name, as_attachment=True)
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
    return jsonify({'result':1})

