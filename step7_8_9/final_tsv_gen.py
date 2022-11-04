import pandas as pd
import urllib.request
import csv
import random

def gen_fake_tsv():
    # load fake data
    fake_papers = pd.read_csv(r'step7_8_9/data/fake_paper_info.csv')

    # load original .tsv to new dataframe
    og_dataframe = pd.read_csv('step7_8_9/data/Final_Output.tsv', delimiter='\t')
    og_dataframe = og_dataframe.drop(columns=['Unnamed: 0', 'Unnamed: 1'])

    col = og_dataframe.columns

    # assign empty pandas dataframe
    fake_data = pd.DataFrame(columns = col)

    # fill in data from fake_papers dataframe
    fake_data['Authors'] = fake_papers['author']
    fake_data['Title'] = fake_papers['title']
    fake_data['Year'] = fake_papers['publish_date'].str[-4:]
    fake_data['Affiliation University'] = fake_papers['affiliation']

    fake_data['Year'] = fake_data['Year'].values.astype('str')
    og_dataframe['Year'] = og_dataframe['Year'].values.astype('str')

    # number list to make fake citations and DOI
    num_list = ['0','1','2','3','4','5','6','7','8','9']

    # create empty lists to populate with sample
    citation_list = []
    findings_list = []
    doi_list = []
    correction_date_list = []
    pub_rates_list = []
    other_journ_list = []
    lab_size_list = []
    deg_level_list = []
    dur_career_list = []
    deg_area_list = []

    # create list of binary values for binary columns
    binary_list = ['','1']

    # iterate through old data to populate lists
    for index,row in og_dataframe.iterrows():
        if row['Citation'] not in citation_list:
            citation_list.append(row['Citation'])
        if row['FINDINGS'] not in findings_list:
            findings_list.append(row['FINDINGS'])
        if row['DOI'] not in doi_list:
            doi_list.append(row['DOI'])
        if row['Correction Date'] not in correction_date_list:
            correction_date_list.append(row['Correction Date'])
        if row['Publication Rates'] not in pub_rates_list:
            pub_rates_list.append(row['Publication Rates'])
        if row['Other Journals'] not in other_journ_list:
            other_journ_list.append(row['Other Journals'])
        if row['Lab Size'] not in lab_size_list:
            lab_size_list.append(row['Lab Size'])
        if row['Author 1 Degree Area'] not in deg_area_list:
            deg_area_list.append(row['Author 1 Degree Area'])
        if row['Degree Level'] not in deg_level_list:
            deg_level_list.append(row['Degree Level'])
        if row['Duration of Career'] not in dur_career_list:
            dur_career_list.append(row['Duration of Career'])

    # populate fake dataframe with randomly selected samples
    for index,row in fake_data.iterrows():
        row['FINDINGS'] = random.choice(findings_list)
        row['Publication Rates'] = random.choice(pub_rates_list)
        row['Correction Date'] = random.choice(correction_date_list)
        row['Other Journals'] = random.choice(other_journ_list)
        row['Lab Size'] = random.choice(lab_size_list)
        row['Author 1 Degree Area'] = random.choice(deg_area_list)
        row['Duration of Career'] = random.choice(dur_career_list)
        row['Degree Level'] = random.choice(deg_level_list)
        row['0'] = random.choice(binary_list)
        row['1'] = random.choice(binary_list)
        row['2'] = random.choice(binary_list)
        row['3'] = random.choice(binary_list)
        row['Retraction'] = random.choice(binary_list)
        if row['Retraction'] != '1':
            row['Correction'] = random.choice(binary_list)
        if row['Retraction'] != '1' and row['Correction'] != '1':
            row['No Action'] = '1'
        row["SUM \nCompleted"] = '1'
        row["Total Authors"] = '1'
        row['Reported'] = '1'
        row['Month'] = '1-Jan'
        for i,r in og_dataframe.iterrows():
            if row['Affiliation University'] == r ['Affiliation University']:
                row['Author 1 Degree Area'] = r['Author 1 Degree Area']
                row['Country'] = r['Country']
            if row['Country'] == r['Country'] and row['Year'] == r['Year']:
                row['Annual Growth Rate %'] = r['Annual Growth Rate %']
                row['Population Density'] = r['Population Density']
                row['Life Expectancy'] = r['Life Expectancy']
                row['Control of Corruption'] = r['Control of Corruption']
                row['Education Expenditure'] = r['Education Expenditure']
                row['Scientific Journal Articles'] = r['Scientific Journal Articles']
                row['AirQuality'] = r['AirQuality']
                row['CountryPopulation'] = r['CountryPopulation']
                row['Compared to Worst AQ Recorded'] = r['Compared to Worst AQ Recorded']
        
    #generate fake citations and DOI by replacing selected numbers with random numbers
    new_citation = []
    new_doi = []

    for x in range(500):
        new_citation.append(random.choice(citation_list).replace('4',random.choice(num_list)).replace('3',random.choice(num_list)))
        new_doi.append(random.choice(doi_list).replace('4',random.choice(num_list)).replace('3',random.choice(num_list)))

    # populate columns with random citation and DOI
    fake_data['Citation'] = new_citation
    fake_data['DOI'] = new_doi

    # join old and new data
    fake_w_og = pd.concat([og_dataframe,fake_data],axis=0)

    # adds column with grover scores
    grover_score = pd.read_csv('step7_8_9/data/GroverScores.csv',header=None)

    fake_w_og['grover_score'] = grover_score[0]

    # export to tsv
    fake_w_og.to_csv('step7_8_9/data/final_hw2.tsv')