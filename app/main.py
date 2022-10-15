from configparser import ConfigParser
import os
import PyPDF2

config_object = ConfigParser()
config_object.read("../setup.cfg")
paths = config_object["paths"]
pdf_names=os.listdir(paths["data"])
pdfFileObj = open(paths["data"]+pdf_names[0], 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
  
# printing number of pages in pdf file
print(pdfReader.numPages)
pageObj = pdfReader.getPage(0)
  
# extracting text from page
print(type(pageObj.extractText()))
  
# closing the pdf file object
pdfFileObj.close()