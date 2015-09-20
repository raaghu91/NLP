__author__ = 'raghu'

import nltk
from nltk import BigramTagger
from nltk.corpus import treebank
from tabulate import tabulate
from operator import itemgetter
import csv

count = {}
total_count = {}
tags_list = ['SNN', 'MISC', 'SRB', 'SVB', 'SJJ']
confusion_matrix = [[0 for x in range(5)] for x in range(5)]

#Evaluation step
def evaluate(actual, predicted):
    global count
    for actual_token,predicted_token in zip(actual, predicted):
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

#Mapping of fine-grained tags to coarse-grained tags
def coarse_map(sentence):
    mapped_sentence = []
    for token in sentence:
        if token[1] in ["NN", "NNS", "NNP", "NNPS", "PRP", "PRP$"]:
            mapped_tag = "SNN"
        elif token[1] in ["VB", "VBP", "VBD", "VBN", "VBZ", "VBG"]:
            mapped_tag = "SVB"
        elif token[1] in ["JJ", "JJR", "JJS"]:
            mapped_tag = "SJJ"
        elif token[1] in ["RB", "RBR", "RBS"]:
            mapped_tag = "SRB"
        else:
            mapped_tag = "MISC"
        mapped_sentence.append((token[0], mapped_tag))

    return mapped_sentence

#Training step
train_sents = treebank.tagged_sents()[:500]
train_coarse_sents = []
for train_sent in train_sents:
    train_coarse_sents.append(coarse_map(train_sent))

t0 = nltk.DefaultTagger('SNN')
t1 = nltk.UnigramTagger(train_coarse_sents, backoff=t0)
t2 = nltk.BigramTagger(train_coarse_sents, backoff=t1)

#Testing step
test_sents = treebank.sents()[500:1000]
tagged_sents = treebank.tagged_sents()[500:1000]
tagged_coarse_sents = []
for tagged_sent in tagged_sents:
    tagged_coarse_sents.append(coarse_map(tagged_sent))
id = 0
file = open('Method-B-predictions.tsv', 'w')
w = csv.writer(file, delimiter='\t')
for actual_tagged_sent, actual_sent in zip(tagged_coarse_sents, test_sents):
    predicted_sent = t2.tag(actual_sent)
    row = id, actual_tagged_sent, predicted_sent
    evaluate(actual_tagged_sent, predicted_sent)
    w.writerow(row)
    id += 1

table = []
total_tokens = 0
total_correct_tokens = 0
# print"Tag",'\t',"total occurrences", '\t', "correctly predicted"
for k1, v1 in total_count.items():
    total_tokens += v1
    total_correct_tokens += count[k1] if k1 in count else 0
    table.append([k1, count[k1]*100/v1 if k1 in count else 0])


print tabulate(sorted(table,key= itemgetter(1), reverse=True),headers = ["Tag", "Accuracy%"])

print "Overall Accuracy:", "%.2f" %((total_correct_tokens) * 100 / float(total_tokens)), "%"

for row, tag in zip(confusion_matrix,tags_list):
    row.insert(0,tag)
tags_list.insert(0, '*')

print tabulate(confusion_matrix, headers=tags_list)
