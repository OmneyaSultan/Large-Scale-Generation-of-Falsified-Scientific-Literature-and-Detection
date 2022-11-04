#import libraries
import random
import csv
import json

#variables to store data
data = [];
titles = [];
affiliations = [];
json_list = [];
randaff = "";
randtitle = "";
json_input0 = [];
json_input1 = [];
json_input2 = [];
json_dicts = [];

############# Step 1 Read TSV and Create Lists To Be Randomized ##################
og_tsv=open('Final_Output.tsv', encoding='ISO-8859-1')
read_tsv= csv.reader(og_tsv, delimiter='\t')

for row in read_tsv:
    data.append(row)

#title list
for i in range(1,len(data)):
    titles.append(data[i][3])

#affiliation list
for i in range(1,len(data)):
    if data[i][25] != "-1":
        affiliations.append(data[i][25])

################ Step 2: Read In JSONL Grover Input ###################
with open("output0.jsonl", 'r') as file:
    json_input0 = list(file);

with open("output1.jsonl", 'r') as file1:
    json_input1 = list(file1);

with open("output2.jsonl", 'r') as file2:
    json_input2 = list(file2);

for element in json_input0:
    result = json.loads(element)
    json_dicts.append(result)

for element in json_input1:
    result = json.loads(element)
    json_dicts.append(result)

for element in json_input2:
    result = json.loads(element)
    json_dicts.append(result)

############### Step 3: Create JSON List ####################
for i in range(1,501):
    randtitle = random.choice(titles)
    randaff = random.choice(affiliations)
    entry = {};
    entry['title'] = randtitle;
    entry['author'] = " "; 
    entry['text'] = json_dicts[i]["gens_article"][0] #from Grover
    entry['publish_date'] = json_dicts[i]["publish_date"]; #from Grover
    entry['affiliation'] = randaff;
    json_list.append(entry);


############## Writing Out JSONL File ##################
with open("Chris.jsonl", 'w') as file:
    for element in json_list:
        file.write(json.dumps(element) + "\n");