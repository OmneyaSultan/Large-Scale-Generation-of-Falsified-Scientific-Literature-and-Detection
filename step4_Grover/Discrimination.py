# Creates the jsonl file that will be passed to the Grover discriminator in order to determine if 
# texts were human- or machine-made.

import csv, json, os

# Initialize variables:
data = [] # Bik data
json_list = [] # Output jsons

# Open the Bik dataset:
og_tsv=open('Final_Output.tsv', encoding='ISO-8859-1')
read_tsv= csv.reader(og_tsv, delimiter='\t')

for row in read_tsv:
    data.append(row)

# Parse the Bik dataset:
for i in range(1, len(data)):
    # Json files with names 1.json, 2.json, etc. contain the text extracted from PDFs
	filepath = 'json_folder/' + str(i) + ".json"
	file = open(os.path.join(os.path.dirname(__file__), filepath), 'r')
	jcontent = json.load(file)

    # Create and fill in json object:
	entry = {}
	entry['title'] = data[i][3]
	entry['domain'] = data[i][5]
	entry['text'] = jcontent["content"]
	entry['summary'] = ''
	entry['authors'] = data[i][2];
	entry['publish_date'] = "01-01-" + str(data[i][6])
	entry['split'] = 'test'
	entry['label'] = 'human'
    # Append to output json list:
	json_list.append(entry)

# Open the Grover falsified text data:
with open("Chris.jsonl", 'r') as file:
    input_list = list(file)

# Parse the Grover falsified text data:
for element in input_list:
    json_obj = json.loads(element)

    # Create and fill in json object:
    entry = {}
    entry["title"] = json_obj["title"]
    entry["text"] = json_obj["text"]
    entry["authors"] = json_obj["author"]
    entry["publish_date"] = json_obj["publish_date"]
    entry["summary"] = ""
    entry["domain"] = ""
    entry["split"] = "test"
    entry["label"] = "machine"
    json_list.append(entry)

# Write to an output jsonl file:
with open("Discrimination_Input.jsonl", 'w') as file:
    for element in json_list:
        file.write(json.dumps(element) + "\n")