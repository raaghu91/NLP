import nltk
from nltk.corpus import treebank
from sys import stdout
import csv
import re


train1_Sent = []
with open ('SC_Final_Questions.txt', 'r') as train_file:
    for line in train_file.readlines():
        train1_Sent.append(line)

#populate the test_Sent list with all the rows in test.tsv file.
train_Sent = []
with open ('SC_answers.txt', 'r') as train_file:
    lines = train_file.readlines()
    x=0
#     option1=lines[x].split('.')[2].strip().split( )[0]
#     print option1
#     exit()
    y=0
    while x<501:
        try:
            option1=lines[x].split('.')[2].strip().split( )[0]
            for sen in train1_Sent[y:y+5]:
                if option1.lower() in sen:
                    print sen
                    train_Sent.append(sen)
            x=x+1
            y=y+5
            print x
            print y
            print option1
            print '------'
        except:
            print x
            print y
            print train_Sent
            exit()

f = open('SC_Final_Answers.txt', 'w')
for i, row in enumerate(train_Sent):
    f.write(row)