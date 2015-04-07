import nltk
from nltk.corpus import treebank
import os
import pickle

#this sets the default encoding to utf-8. the train_set contains characters which are not ASCII. So setting the default encoding to "utf-8"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#populate the train_Sent list with all the rows in train.tsv file.
train_Data = []
for root, directories, files in os.walk('Training Data/hi'):
    for filename in reversed(files):
#         print filename
        with open (os.path.join(root, filename), 'r') as train_file:
            train_Data.append(train_file.read())


#populate the questions to be tested against into test_data_questions list.
test_data_questions = []
with open ('Test Data/MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.questions.txt', 'r') as test_ques_file:
    test_data_questions.append(test_ques_file.read())
    
#tag each word in the train_Data
postag_Sent = []
for i,sentence in enumerate(train_Data):
    token_Sent = nltk.sent_tokenize(sentence)
    token_Word = [nltk.word_tokenize(sent) for sent in token_Sent]
    pos_Sent = [nltk.pos_tag(sent) for sent in token_Word]
    postag_Sent.append(pos_Sent)
    
# using a default tagger.
default_tagger = nltk.DefaultTagger('NN')

# build the model using the Unigram tagger on trained data with back_off model as default tagger.
t_unigram_tagger = nltk.UnigramTagger(postag_Sent, backoff=default_tagger)

# build a model using the Bigram tagger on trained data with back_off model as Unigram tagger.
t_bigram_tagger = nltk.BigramTagger(postag_Sent, backoff=t_unigram_tagger)

t_trigram_tagger = nltk.TrigramTagger(postag_Sent, backoff=t_bigram_tagger)

print t_trigram_tagger.evaluate(test_data_questions[0][0])
print t_trigram_tagger.evaluate(test_data_questions[0][1])
print t_trigram_tagger.evaluate(test_data_questions[0][2])
print t_trigram_tagger.evaluate(test_data_questions[0][3])
print t_trigram_tagger.evaluate(test_data_questions[0][4])

