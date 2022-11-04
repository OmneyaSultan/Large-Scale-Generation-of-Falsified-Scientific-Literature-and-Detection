GROUP: Seize the
Data
---------------------




## TABLE OF CONTENTS
---------------------
- Overview
- Libraries imported
- Control_Script.py
- Extracting Original Data 
- Grover
- Fake Image Generator
- Image Caption Generator
- LaTeX
- Updating TSV


--------------------------------
## OVERVIEW

In this project, we further explored the given 'Big et al Media' dataset in order to generate 500 fake scientific articles. The following tasks included: extracting text from the original articles in the dataset, using grover to generate fake text, using DCGAN to generate fake images, using tike-dockers to create fake captions, using LaTeX to combine the different parts into pdfs for the fake articles, and finally updating the original tsv file to include the 500 fake articles along with fake ancillary features.

'Final_Output_v2.tsv' is our final updated tsv file with all added attributes- it can be found in the Expected_Output directory.

The following ReadMe file will explain what each program requires and how it runs. Due to the various programs that were used to complete this project, the ReadMe file is divided in a way that explains each program.

--------------------------------

## LIBRARIES IMPORTED

- csv 
- json
- numpy
- tensorflow-gpu
- tensorboard 
- random
- os
- glob
- requests
- Fitz
- slugify
--------------------------------

## Control_Script

The control script will run Image Caption Generator and ……

Running Control_Script.py along with ‘—Test_Captions’ as an argument will generate captions for 1/4th of the fake images. The final output will be ‘Fake_Images_Final.csv’. Uses static file ‘Fake_Images.csv’ which contains the name of the images and the URLs.

Running Control_Script.py along with ‘—Generate_Captions’ as an argument will generate captions for all 500 fake images in batches of 4. The final output will be ‘Fake_Images_Batch1.csv’.  This may take about 20 minutes to run. Uses static file ‘Fake_Images.csv’ which contains the name of the images and the URLs.

All output .tsv files will be found in TEAM_SEIZE_THE_DATA_DSCI550_HW_BIGDATA directory as they are generated.


--------------------------------
## EXTRACTING ORIGINAL DATA

The dataset has been split so each spreadsheet has 30 papers to avoid crashing web driver and reduce chance of getting blocked

The code is meant to be run with one 30 paper chunk at a time as follows:

Go through “BIK_Researchgate copy x.tsv” in sequence. For each tsv save a copy and rename as “BIK_Researchgate.tsv” (since this is the file name the code is expecting)

Its important to use these datasets as is because I added a column called “serial” which I am using to name the papers as they are downloaded per their serial number in the dataset

--------------------------------
### Installing Chrome Webdriver

`$ sudo apt-get install unzip`
`$ wget -N http://chromedriver.storage.googleapis.com/2.29/chromedriver_linux64.zip -P ~/Downloads`
`$ unzip ~/Downloads/chromedriver_linux64.zip -d ~/Downloads`

moved chromedriver from downloads to usr/local/share
`$ sudo mv -f ~/Downloads/chromedriver /usr/local/share/`

`$ sudo chmod +x /usr/local/share/chromedriver`

moved it again to usr/local/bin
`$ sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver`

Note: when I first tried to do this (move from local share to local bin) I got operation not permitted, which I resolved by giving full disk access to terminal in privacy settings

`$ sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver`


The path I actually wound up with is usr/local/bin/chromedriver

To find chromedriver version:

`Chromedriver —version`

At which point I got an error message that the developer is not trusted so I removed quarantine using: 

`xattr -d com.apple.quarantine /usr/local/bin/chromedriver`



--------------------------------

### Installing selenium: 

`Pip install selenium`

--------------------------------
### Installing Tika

`Pip install tika`

--------------------------------
Then test Tika with any file

Initializing Tika for the first time:

`import tika`

`tika.initVM()`

`from tika import parser`

`parsed = parser.from_file('file.pdf')`

`print(parsed["metadata"])`

`print(parsed["content"])`


IMPORTANT: get the path where its being installed!
--------------------------------
Every time after that:

`import os`

Set tika environment variables to path where tika was first installed to avoid downloading 60 MB of tika from the server every time you run your code

`os.environ['TIKA_SERVER_JAR'] = "file:///var/folders/6f/jn6jftmx52n84g99clgmg60w0000gp/T/tika-server.jar"`
`os.environ['TIKA_PATH'] = "<file:///var/folders/6f/jn6jftmx52n84g99clgmg60w0000gp/T/"`



`#!/usr/bin/env python`

`import tika`

`tika.initVM()`

`from tika import parser`

`parsed = parser.from_file('file.pdf')`

`print(parsed["metadata"])`

`print(parsed["content"])`
--------------------------------
### Converting pdfs to JSONs

- The Jupyter Notebook submitted in this HW titled “Output Jsons from pdfs” was used for the conversion. A personal Google drive of one of the group members, where the pdfs had been uploaded in a folder named “pdf_folder” that was shared with the rest of the group, is first mounted when the notebook is run. 
- The code grabs the pdfs in the “pdf_folder” on Google drive and uses Tika Python to convert each pdf into a JSON file, name it the same name as the pdf file, then save it in a folder on Google drive named “json_folder”, which was also shared with the whole group.
--------------------------------
## GROVER

There are four python scripts and two Google Colab notebooks associated with the Grover steps in this project. 

Grover generation:
- CreateJsonl.py: This file accesses the Bik dataset and puts the data into json objects in the format required by the Grover generator. A jsonl file is created, which is used to run Grover_generation.ipynb. The installed libraries are csv and json.
- Grover_generation.ipynb: This file runs the Grover generator. The installed libraries come from Rowan Zellers’ GitHub repository, as well as numpy, tensorflow-gpu, and tensorboard. The Grover generator is run in a loop 3 times, to generate 642 fake articles.
- GenFakeTitle.py: This file accesses the Grover generator’s output and uses that information to create a jsonl file with the new articles. A fake title is generated for each article by randomly sampling the existing Bik dataset. The installed libraries are random, csv, and json.
Grover discrimination:
- Discrimination.py: This file accesses all of the data from the Bik dataset in combination with the 500 generated articles, and merges them into a jsonl file in the format required by the Grover generator. The installed libraries are os, csv, and json.
- Grover_discrimination.ipynb:  This file runs the Grover discriminator, using pre-trained models. It gives a numpy file as output, which gives the prediction whether each file is machine or human. The installed libraries come from Rowan Zellers’ GitHub repository, as well as numpy, tensorflow-gpu, and tensorboard. 
- GetColumn.py: This file parses the numpy file produced by Grover_discrimination.ipynb, and writes the data to a csv file for later use. The installed libraries are csv and numpy.
--------------------------------
## FAKE IMAGE GENERATOR  (DCGAN)

Contains: step5_1_directory_image_extractor.py , step5_2_dcgan.ipynb

File: Step5_1_directory_image_extractor.py
Required libraries:

import fitz #PyMuPDF
import io
from PIL import Image
import os.path
from slugify import slugify
import glob

Description: 
This program extracts from .jpg images located in the PATH: dcgan_images/dcgan_input and outputs fake image results into PATH: dcgan_images/dcgan_output
The program replaced any pooling layers from each .jpg file located in the dcgan_input folder with strided convolutions (discriminator) and fractional-strided convolutions(generator) using batch norm in both the generator and the discriminator.
***Note: This program can take between 3-4 hours from execution to completion.
--------------------------------
File: step5_2_dcgan.ipynb
Required libraries:
import os
import time
import tensorflow as tf
import numpy as np
from glob import glob
import datetime
import random
from PIL import Image
import matplotlib.pyplot as plt
%matplotlib inline

Description: 
Step 1: Program loops through all .pdf files within folder 'pdfs', reading metadata.title information from each 
document saving it in variable: Pdf_title.

Step 2: Program loops through each .pdf page and extracts all images from each document

Step 3: Program uses metadata.title (paper name) created in Step 1 to create a new directory named after
the papername. 

Step 4: Program converts all non-PNG file extensions to PNG and saves individual .png image files
into the correct directory that correlates with the .pdf file (paper name) it was extracted from.


--------------------------------
## IMAGE CAPTION GENERATOR

Installations that worked for my code to run:
- Install Dockers 4.6.1: https://docs.docker.com/desktop/mac/install/
- Download Tensorflow: https://www.tensorflow.org/install
- Download tika-dockers: https://github.com/USCDataScience/tika-dockers
	Edited tiki-docker code based on this GitHub suggestion: https://github.com/USCDataScience/tika-dockers/pull/2/files
- Download img2text: https://github.com/USCDataScience/img2text
- Download Tika 2.3.0: https://tika.apache.org/download.html
- Download Apache-maven 3.8.5: https://maven.apache.org/download.cgi

import glob
import csv
import requests

Tika-Dockers must be running:
	docker build -f Im2txtRestDockerfile -t uscdatascience/im2txt-rest-tika .
	docker run -it -p 8764:8764 uscdatascience/im2txt-rest-tika

Relevant code for image captioning is in the ‘Image_Caption’ Directory.
‘Image_Caption/Expected_Output’ contains the tsv file with the saved captions that was used in LaTeX.

How the code works in GenerateCaptions.py:
1. create_img_csv():
	*Looks at the 500 fake images that were created with DCGAN. 
	*Extracts the name of the files and saves them in a csv file ‘Fake_Images.csv’
	*The images were manually uploaded to postimage.org and the URLs for the images were manually 	added to ‘Fake_Images.csv’
2. get_caption():
	*This function retrieved the caption for each image
	*input: URL for the image
	*output: the first caption generated by tika-dockers which normally had the highest confidence
3. save_captions
	*Iterated through ‘Fake_Images.csv’ and used get_caption() on the URLs of each image.
	*Saved lists including name, url, and caption in a list named ‘fake_images’
	*input: csv_file (‘Fake_Images.csv’)
	*output: dictionary with image name as key and caption as value, along with ‘fake_images’ list
4. output_caption_csv():
	*iterates through the list created by save_captions and creates/updates the final csv_file 	‘Fake_Images_Final.csv’
	*input: fake_images list, name of output file
	*output: tsv file with the name, url and captions of the 500 fake images.


--------------------------------
## LATEX

- For this step - Faker, pyLaTex must be installed via pip install. Also, a pdf compiler must be installed like Miktex which can be downloaded from miktex.org.
- Prior to running Latex, the fake_name_gen.py script must be run to generate the input for creating the fake .pdfs. This script can be found in the ‘step7_8_9’ directory.
- The fake_name_gen.py creates a .csv file containing the title of a work, an author name which is randomly generated when the script is ran, text that was generated from Grover step, publish dates and affiliation which were randomly sampled from the original dataset, filename of the image which was provided after the imaging step as well as captions.
- Output for fake_name_gen.py is named ‘fake_paper_info.csv’ and can be found in ‘data’ directory within ‘steps7_8_9’ directory.
- fake_paper_gen.py can then be ran once the output has been created. However since the output from the previous script has been provided, users can choose to run this step with the given .csv as input.

*NOTE: As the above script generates 500 .pdf files, this script can take approximately 20 minutes to run depending on system configuration.

- The script accesses image files contained in the ‘500_fake_images’ directory within the ‘falsified_media’ directory and generates pdfs using data from the ‘fake_paper_info.csv’ file in the ‘data directory’.
- .pdf and .tex files are output into the ‘falsified_media’ directory. .log and .aux files are created with metadata.



--------------------------------
## UPDATING TSV FILE

- Once all steps have been completed, final_tsv_gen.py can be accessed to combine all data (new and old) into a single Final_Output_v2.tsv file which can be found in the ‘data’ directory within the ‘step7_8_9’ directory.
- The .tsv file will include all features from the original dataset with an additional 500 records filled with fake information.
- An additional column will be added to show the Grover scores for each record. These scores indicate whether Grover was able to detect if the document was fake.













