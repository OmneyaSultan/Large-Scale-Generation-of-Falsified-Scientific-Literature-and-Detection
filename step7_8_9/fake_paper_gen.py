from pylatex import Document, Section, Subsection, Command, Figure
from pylatex.utils import italic, NoEscape
from pylatex.package import Package
import numpy as np
import os
import pandas as pd
import urllib.request

fake_papers = pd.read_csv(r'step7_8_9/data/fake_paper_info.csv')

# function adds text to document
def fill_document(doc,text):
    """Add a section, a subsection and some text to the document.
    :param doc: the document
    :type doc: :class:`pylatex.document.Document` instance
    """
    with doc.create(Section('Abstract')):
        doc.append(text)

def gen_fake_pdf():
    # iterate through dataframe to generate fake papers
    for index,row in fake_papers.iterrows():
        # Document with `\maketitle` command activated
        doc = Document()
            
        doc.packages.append(Package('authblk'))
        doc.preamble.append(Command('title', row['title']))
        doc.preamble.append(Command('author', row['author']))
        doc.preamble.append(Command('affil', row['affiliation'].strip()))
        doc.preamble.append(Command('date', row['publish_date']))
        doc.append(NoEscape(r'\maketitle'))

        # call function to fill document with text
        fill_document(doc,row['text'].strip())

        # add fake image with caption
        with doc.create(Subsection('Image Analysis')):
            with doc.create(Figure(position='h!')) as image:
                image.add_image(filename='500_fake_images/'+row['filename'], width='150px')
                image.add_caption(row['caption'])

        # export as pdf
        doc.generate_pdf('falsified_media/paper' + str(index), clean_tex=False,compiler="pdflatex")

        # create .tex file
        tex = doc.dumps()  # The document as string in LaTeX syntax