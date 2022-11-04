#import libraries
import csv
import json

#variables to store data
data = []
headers = [];
json_list = [];

##read the tsv file and store the information
og_tsv=open('Final_Output.tsv', encoding='ISO-8859-1')
read_tsv= csv.reader(og_tsv, delimiter='\t')

for row in read_tsv:
    data.append(row)

##create dictionaries for each row in the tsv containing the data Grover needs to run
##and append that to a list
for i in range(1, len(data)):

    filename = str(i) + ".json";
    file = open(filename);
    jcontent = json.load(file);

    entry = {};
    entry['title'] = data[i][3];
    entry['domain'] = data[i][5];
    entry['text'] = jcontent["content"]
    if data[i][12] == "":
        entry['summary'] = "Summary not provided."
    else:
        entry['summary'] = data[i][12]
    entry['authors'] = data[i][2];
    entry['publish_date'] = "01-01-" + str(data[i][6])
    json_list.append(entry);


#turn that list into a jsonl file that Grover will then take in as input for generation.
with open("completejsonl.jsonl", 'w') as file:
    for element in json_list:
        file.write(json.dumps(element) + "\n")