# Import statements
import requests
import pandas as pd
import os, itertools, argparse, csv
from requests import ConnectionError
import time
from time import sleep
import ast
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




# --------------------------Read TSV File and Create Dictionaries Section --------------------------------------------
        
#variables to store data
og_dataset = {}
data = [];

#Read TSV File
og_tsv=open('BIK_Researchgate.tsv', encoding='ISO-8859-1')
read_tsv= csv.reader(og_tsv, delimiter='\t')

#put all of the rows in the tsv into a list
for row in read_tsv:
    data.append(row);
    
#put the headers of the tsv in a separate list
headers = data.pop(0);

#go through each column in the dataset and store it into a dictionary where the key is the header and the value
#is a list of all of the values in that column.
for i in range(len(headers)):
    interim = [];
    for j in range(len(data)):
        interim.append(data[j][i])
    og_dataset[headers[i]] = interim;


# --------------------------get DOIs in a list--------------------------------------------
dois=dict()

length_of_lst=len(og_dataset["DOI"])
for i in range(length_of_lst):
  col=((og_dataset["serial"])[i])
  row=((og_dataset["DOI"])[i])
  dois[col]=row
# ----------------------------------------------------------------------

os.mkdir('html_folder')

os.chdir('html_folder')


# ----------------------------use selenium to grab url using doi------------------------------------------

#create an empty list to hold all the paper URLs
urls = dict()

#get the urls using the dois
driver = webdriver.Chrome('chromedriver')



#get url for each doi in the doi list
for serial,doi in dois.items():
  try: 
    driver.get('https://dx.doi.org/')
    inputElement = driver.find_element_by_name("hdl")
    inputElement.send_keys(doi)
    inputElement.send_keys(Keys.ENTER)
    #time.sleep(6)
    urls[serial]=(driver.current_url)
    html = driver.page_source
    papername=serial+".html"
    with open(papername, "a") as f:
      f.write(html)  

  except: continue
driver.close



#--------------------------start up tika-------------------

os.environ['TIKA_SERVER_JAR'] = "file:///var/folders/6f/jn6jftmx52n84g99clgmg60w0000gp/T/tika-server.jar"
os.environ['TIKA_PATH'] = "<file:///var/folders/6f/jn6jftmx52n84g99clgmg60w0000gp/T/"


#!/usr/bin/env python

import tika
tika.initVM()
from tika import parser
#--------------------------use tika------------------

#use Tika to get url of pdf file from html saved using selenium
pdf_url_lst=dict()

for filename in os.listdir():

  try:

    parsed = parser.from_file(filename)
    pdf_url_lst[filename]=((parsed["metadata"])['citation_pdf_url'])

  except: continue


#--------------------------get list of available pdf urls------------------

os.chdir('..')

os.mkdir('pdf_folder')

os.chdir('pdf_folder')

#use URL of pdf to download file
for htmlname,file_url in pdf_url_lst.items():
    r = requests.get(file_url, stream = True)
    
    pdfname=htmlname.replace('.html','.pdf')
    


    with open(pdfname, "wb") as file: 
      for block in r.iter_content(chunk_size = 1024): 
        if block: 
          file.write(block)










