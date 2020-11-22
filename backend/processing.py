from bs4 import BeautifulSoup
import re



def cleanText(text):
    text = BeautifulSoup(text, "lxml").text
    text = re.sub(r'\|\|\|', r' ', text) 
    text = re.sub(r'http\S+', r'<URL>', text)
    text = re.sub(r'\+','',text)
    text = text.lower()
    #text = text.replace('x', '')


    return text
