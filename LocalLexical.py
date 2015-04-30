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
for root, directories, files in os.walk('Training Data/Holmes_Training_Data'):
    for filename in reversed(files):
#         print filename
        with open (os.path.join(root, filename), 'r') as train_file:
            train_Data.append(train_file.read())


#populate the questions to be tested against into test_data_questions list.
test_data_questions = []
with open ('Test Data/MSR_Sentence_Completion_Challenge_V1/Data/Holmes.machine_format.questions.txt', 'r') as test_ques_file:
    test_data_questions.append(test_ques_file.read())

test_ques = test_data_questions[0].split('.')
ques_List = []
for i,question in enumerate(test_ques[0:20]):
    token_Sent = nltk.sent_tokenize(question)
    token_Word = [nltk.word_tokenize(sent) for sent in token_Sent]
    pos_Sent = [nltk.pos_tag(sent) for sent in token_Word]
    ques_List.append(pos_Sent)
    
# print ques_List[0]
print 'tagging testing data complete'

#tag each word in the train_Data
postag_Sent = []
for i,sentence in enumerate(train_Data):
    pos_Sent = []
    print 'file' + str(i)
    try:
        token_Sent = nltk.sent_tokenize(sentence)
        token_Word = [nltk.word_tokenize(sent) for sent in token_Sent]
        pos_Sent = [nltk.pos_tag(sent) for sent in token_Word]
        postag_Sent.append(pos_Sent)
    except:
        print 'exception occurred'
        print pos_Sent
print 'tagging training data complete'

#print postag_Sent

#each file is a index in list. postag_Sent[0] is first file and so on. 
# print len(postag_Sent[0])
# exit()

# using a default tagger.
default_tagger = nltk.DefaultTagger('NN')

# build the model using the Unigram tagger on trained data with back_off model as default tagger.
t_unigram_tagger = nltk.UnigramTagger(postag_Sent[0], backoff=default_tagger)

# build a model using the Bigram tagger on trained data with back_off model as Unigram tagger.
t_bigram_tagger = nltk.BigramTagger(postag_Sent[0], backoff=t_unigram_tagger)

t_trigram_tagger = nltk.TrigramTagger(postag_Sent[0], backoff=t_bigram_tagger)


print 'model is successfully created'
print t_trigram_tagger.evaluate(ques_List[0])
print t_trigram_tagger.evaluate(ques_List[1])
print t_trigram_tagger.evaluate(ques_List[2])
print t_trigram_tagger.evaluate(ques_List[3])
print t_trigram_tagger.evaluate(ques_List[4])

print '-------------------------------------------'
print t_trigram_tagger.evaluate(ques_List[5])
print t_trigram_tagger.evaluate(ques_List[6])
print t_trigram_tagger.evaluate(ques_List[7])
print t_trigram_tagger.evaluate(ques_List[8])
print t_trigram_tagger.evaluate(ques_List[9])

print '-------------------------------------------'

print t_trigram_tagger.evaluate(ques_List[10])
print t_trigram_tagger.evaluate(ques_List[11])
print t_trigram_tagger.evaluate(ques_List[12])
print t_trigram_tagger.evaluate(ques_List[13])
print t_trigram_tagger.evaluate(ques_List[14])

print '-------------------------------------------'
print t_trigram_tagger.evaluate(ques_List[15])
print t_trigram_tagger.evaluate(ques_List[16])
print t_trigram_tagger.evaluate(ques_List[17])
print t_trigram_tagger.evaluate(ques_List[18])
print t_trigram_tagger.evaluate(ques_List[19])

print '-------------------------------------------'

