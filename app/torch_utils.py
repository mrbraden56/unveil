from ast import List
from configparser import ConfigParser
from lib2to3.pgen2.tokenize import tokenize
import os
import PyPDF2
from tokenizers import decoders, models, normalizers, pre_tokenizers, processors, trainers, Tokenizer
import nltk
nltk.download('punkt')
from nltk import tokenize
from nltk.tokenize import BlanklineTokenizer
import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import pandas as pd

class SummarizeParagraph:
    def __init__(self, pdf_name: str, upload_folder: str, model, tokenizer) -> None:
        self.pdf_name: str = pdf_name
        self.upload_folder: str = upload_folder
        self.model_trained = model.from_pretrained("saved_model")
        self.tokenizer_trained = tokenizer.from_pretrained("saved_model")
        self.peg_tokenizer=PegasusTokenizer.from_pretrained("google/pegasus-xsum")
        self.peg_model=PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")

    def classify_paragraph(self, model, tokenizer, paragraph):
        input_ids = []
        attention_masks = []
        encoded_dict=tokenizer.encode_plus(
                                paragraph,
                                add_special_tokens = True,
                                max_length = 500,
                                pad_to_max_length = True,
                                return_attention_mask = True,
                                return_tensors = 'pt',
                        )
        input_ids.append(encoded_dict['input_ids'])
        attention_masks.append(encoded_dict['attention_mask'])
        result = model(input_ids[0], 
                            token_type_ids=None, 
                            attention_mask=attention_masks[0],
                            return_dict=True)
        result=int(torch.argmax(result.logits))
        if result==1: return True
        else: return False

    def summarize(self, paragraph):
        tokens = self.peg_tokenizer(paragraph, truncation=True, padding="longest", return_tensors="pt")
        output = self.peg_model.generate(**tokens)
        summary=self.peg_tokenizer.decode(output[0])
        return summary


    def run(self):
        pdfFileObj = open(self.upload_folder+self.pdf_name, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        number_of_pages=pdfReader.numPages
        risk_dic={"Original": [], "Summarized": []}
        for i in range(0,number_of_pages):
            pageObj = pdfReader.getPage(i)
            pdf_page=pageObj.extractText()
            paragraphs = BlanklineTokenizer().tokenize(pdf_page)
            for paragraph in paragraphs:
                result=self.classify_paragraph(self.model_trained, self.tokenizer_trained, paragraph)
                if result:
                    summary=self.summarize(paragraph)
                    risk_dic["Original"].append(paragraph)
                    risk_dic["Summarized"].append(summary)
                    print(paragraph)
                else:
                    continue
            print(f"Page {i} of {number_of_pages}")
        risk_dic = pd.DataFrame.from_dict(risk_dic)
        return risk_dic