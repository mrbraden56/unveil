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
import mysql.connector

class DB:
    def __init__(self) -> None:
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="traindatabase"
        )
        self.mycursor=self.db.cursor()
        #table called textdata

    def get_values(self):
        self.mycursor.execute("select * from textdata")
        return self.mycursor.fetchall()

def main():
    config_object = ConfigParser()
    config_object.read("../setup.cfg")
    paths = config_object["paths"]
    db=DB()
    db_values=db.get_values()

if __name__ == "__main__":
    main()