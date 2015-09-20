__author__ = 'raghu'

import nltk
import csv
from nltk import BigramTagger
from collections import Counter
from tabulate import tabulate
from nltk.corpus import treebank
from operator import itemgetter

count = {}
total_count = {}
confusion_matrix = [[0 for x in range(11)] for x in range(11)]

#tags for which the confusion matrix has to be reported
tags_list = ['JJ', 'NN', 'NNP', 'NNPS', 'RB', 'RP', 'IN', 'VB', 'VBD', 'VBN', 'VBP']

#Evaluatioin step
def evaluate(actual, predicted):
    global count, confusion_matrix
    for actual_token,predicted_token in zip(actual, predicted):
        if actual_token[1] in tags_list and predicted_token[1] in tags_list:
            confusion_matrix[tags_list.index(actual_token[1])][tags_list.index(predicted_token[1])] += 1
        if actual_token[1] in total_count:
            total_count[actual_token[1]] += 1
        else:
            total_count[actual_token[1]] = 1
        if actual_token[1] == predicted_token[1]:
            if actual_token[1] in count:
                count[actual_token[1]] += 1
            else:
                count[actual_token[1]] = 1




#Training section
train_sents = treebank.tagged_sents()[:500]
t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(train_sents, backoff=t0)
t2 = nltk.BigramTagger(train_sents, backoff=t1)

#Testing section
test_sents = treebank.sents()[500:1000]
tagged_sents = treebank.tagged_sents()[500:1000]
id = 0
file = open('part-1-predictions.tsv', 'w+')
w = csv.writer(file,delimiter = '\t')
for actual_tagged_sent, actual_sent in zip(tagged_sents, test_sents):
    predicted_sent = t2.tag(actual_sent)
    row = id, actual_tagged_sent, predicted_sent
    evaluate(actual_tagged_sent, predicted_sent)
    # count_predicted(predicted_sent)
    w.writerow(row)
    id += 1



table = []
total_tokens = 0
total_correct_tokens = 0
for k1, v1 in total_count.items():
    total_tokens += v1
    total_correct_tokens += count[k1] if k1 in count else 0
    table.append([k1, count[k1]*100/v1 if k1 in count else 0])



# print tabulate(sorted(table,key= itemgetter(3), reverse=True),headers = ["Tag","total occurrences","correctly predicted","Accuracy%"])
print tabulate(sorted(table, key=itemgetter(1), reverse=True), headers=["Tag", "Accuracy%"])

print "Overall Accuracy:", "%.2f" %((total_correct_tokens) * 100 / float(total_tokens)), "%"


for row, tag in zip(confusion_matrix,tags_list):
    row.insert(0,tag)
tags_list.insert(0, '*')

print("Confusion matrix:")
print tabulate(confusion_matrix, headers=tags_list)






