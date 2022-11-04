#import libraries
import numpy
import csv

#list to hold probablities
probs = []

#load numpy file
numbers = numpy.load("test-probs.npy")


#loop through first column to get machine probabilities
for i in range(0,len(numbers)):
    interim = [];
    interim.append(numbers[i][0])
    probs.append(interim)

#write to a csv file
with open('GroverScores.csv', 'w') as file:
    write = csv.writer(file)
    write.writerows(probs);

