import nltk
from nltk.corpus import treebank
from sys import stdout
import csv
import re

#populate the test_Sent list with all the rows in test.tsv file.
train_Sent = []
with open ('SC_questions.txt', 'r') as train_file:
    lines = train_file.readlines()
#     print lines[1].split('.')[1].strip()
#     exit()
    x=0
    while x<3507:
        try:
            question=lines[x]
            x=x+1
            option1=lines[x].split('.')[1].strip()
            x=x+1
            option2=lines[x].split('.')[1].strip()
            x=x+1
            option3=lines[x].split('.')[1].strip()
            x=x+1
            option4=lines[x].split('.')[1].strip()
            x=x+1
            option5=lines[x].split('.')[1].strip()
            x=x+2
            print x
            train_Sent.append(question.replace('______','[' +option1 +']'))
            train_Sent.append(question.replace('______','[' +option2 +']'))
            train_Sent.append(question.replace('______','[' +option3 +']'))
            train_Sent.append(question.replace('______','[' +option4 +']'))
            train_Sent.append(question.replace('______','[' +option5 +']'))
        except:
            print x
            exit()

f = open('SC_Final_Questions.txt', 'w')
for i, row in enumerate(train_Sent):
    f.write(row)