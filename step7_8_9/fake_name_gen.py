import pandas as pd
import urllib.request
import csv
import random
from faker import Faker

def gen_fake_names():
    # create list of fake names
    fake = Faker()
    fake_name_list = []

    for x in range(500):
        fake_name_list.append(fake.name())
	
    # load data for fake papers
    fake_papers = pd.read_json (r'step7_8_9/data/fake_data.jsonl',lines=True)

    # add fake authors to dataframe
    fake_papers['author'] = fake_name_list

    # adjust encoding for compatibility with pylatex
    for index,row in fake_papers.iterrows():
        row['text'] = row['text'].encode("ascii", "ignore")
        row['text'] = row['text'].decode()
        row['title'] = row['title'].encode("ascii", "ignore")
        row['title'] = row['title'].decode()
        row['affiliation'] = row['affiliation'].encode("ascii", "ignore")
        row['affiliation'] = row['affiliation'].decode()

    # load fake images table
    fake_images = pd.read_csv (r'step7_8_9/data/Fake_Images_Final.csv')

    # extra record was assigned as header. renaming
    fake_images = fake_images.rename(columns={"samples_5_0.png": "filename", 
                                              "https://i.postimg.cc/BvMkzZtw/samples-5-0.png": "url", 
                                              "A Black And White Photo Of A Young Boy":"caption"})

    # join fake_papers table with fake_images
    fake_papers = fake_papers.join(fake_images)
    fake_papers.to_csv('step7_8_9/data/fake_paper_info.csv')