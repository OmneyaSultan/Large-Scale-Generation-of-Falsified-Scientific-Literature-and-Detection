#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Group: Sieze the Data
Course: DSCI 550 - Spring 2022
Date: April 2022

Description:

Step 1: Program loops through all .pdf files within folder 'pdfs', reading metadata.title information from each 
document saving it in variable: Pdf_title.

Step 2: Program loops through each .pdf page and extracts all images from each document

Step 3: Program uses metadata.title (paper name) created in Step 1 to create a new directory named after
the papername. 

Step 4: Program converts all non-PNG file extensions to PNG and saves individual .png image files
into the correct directory that correlates with the .pdf file (paper name) it was extracted from.
       
"""

#----------------- Python Libraries Needed To Run Program --------
import fitz #PyMuPDF
import io
from PIL import Image
import os.path
from slugify import slugify
import glob
 
#----------------- PDF Image Scraper / Directory Maker -----------

#loops through all .pdf files located in pdfs folder
pdf = glob.glob('pdfs/*.pdf')

#Uses PyMuPDF fitz to gather metadata title information from individual pdf files 
for file in pdf:
    pdf_file = fitz.open(file)
    #obtains the .pdf file name
    pdf_title = (pdf_file.metadata['title'])
    #loops through all pages located in each .pdf file 
    for page_index in range(len(pdf_file)):
        # Obtains the .pdf file page
        page = pdf_file[page_index]
        image_list = page.getImageList()
        
        # prints the number of images located on each page per article
        if image_list:
            #displays for image tracking status
            print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        else:
            #displays if no images are found on a particular .pdf page
            print("[!] No images found on page", page_index)
        for image_index, img in enumerate(page.getImageList(), start=1):
            # get the XREF of the image
            xref = img[0]
            # extract the image bytes
            base_image = pdf_file.extractImage(xref)
            image_bytes = base_image["image"]
            # get the image extension of image
            image_ext = base_image["ext"]
            # load it to PIL
            image = Image.open(io.BytesIO(image_bytes))
            #creates a new directory named /pdf_images and concatnates with pdf_title meta info
            dir_path = os.path.join(r"pdf_images", slugify(pdf_title))
            #prints directory information during creation process
            print('making', dir_path)
            #checks if directory is created
            if not os.path.exists(dir_path):
                #creates directory if directory isn't created as .pdf paper name
                os.mkdir(dir_path)
                #saves images in directory based on paper name it was scraped from
                image.save(open(os.path.join(dir_path, f"-image-page{page_index+1}_{image_index}.png"),"wb"))
            else:
                #converts png to rgb for pixel reasons and then saves it into the correct directory
                image.convert('RGB').save(open(os.path.join(dir_path, f"-image-page{page_index+1}_{image_index}.png"), "wb"), optimize=True)