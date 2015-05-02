# from gensim.models import word2vec
# # b = Word2Vec(brown.sents())
# # mr = Word2Vec(movie_reviews.sents())
# # t = Word2Vec(treebank.sents())
# 
# # print b.most_similar('money', topn=5)
# # model = Word2Vec.load_word2vec_format('/home/dontubalu/Downloads/GoogleNews-vectors-negative300.bin.gz',binary=True)
# # print model['ravenous']
# # print model.similarity('bossy', 'magisterial')
# 
# import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# 
# sentences = word2vec.Text8Corpus('text8')
#  
# model = word2vec.Word2Vec(sentences, size=200)
# 
# model.most_similar(['man'])

from nltk.corpus import wordnet
from itertools import product
from requests import get
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import os

# def merge_Wiki_Data():
#     dir="wikiData/"
#     files = os.listdir(dir)
#     with open('wikiData_Output/wiki_Data.txt', 'w') as outfile:
#         for fname in files:
#             with open(dir+fname) as infile:
#                 outfile.write(infile.read())
#                 
# merge_Wiki_Data()
# exit()

wiki_Data_List=[]
def prepare_Data():
    dir="wikiData_Output/"
    files = os.listdir(dir)
    for fname in files:
        with open(dir+fname) as infile:
            file_Data=infile.read()
            sentences=file_Data.split('.')
            for sentence in sentences:
                word_List=[word for word in sentence.strip(' ').split(' ') if word != ' ']
                wiki_Data_List.append(word_List)

# prepare_Data()
# print wiki_Data_List
# exit()

broken_Words={}
prepare_Data()
model=Word2Vec(wiki_Data_List, min_count=1)

def cosine_Similarity_Words(word, option, question_Count):
    try:
#         sentences = [['first','sentence'],['second','sentence']]
        
#         model = Word2Vec.load_word2vec_format('wikiData_Output/wiki_Data_1.txt', binary=False)  # C text format
    #     model.similarity('woman', 'man') #
#         print model['clip'] #raw numpy vector of a word  
    #     model.n_similarity(['sushi', 'shop'], ['japanese', 'restaurant'])#cos similarity between two sets of words
        return model.similarity(word, option)#cos similarity between two words
    except:
        print 'Exception'
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((word, option))
        
# 
# print cosine_Similarity_Words('first', 'sentence', 0)
# exit()
#Get the stop word list from NLTK corpus
stop_Word_List = set(stopwords.words('english'))

questions_Sent=[]
with open('SC_Final_Questions.txt','r') as questions_file:
    lines = questions_file.readlines()
    for line in lines:
        questions_Sent.append(line)
        
answers_Sent=[]
with open('SC_Final_Answers.txt','r') as answers_file:
    lines = answers_file.readlines()
    for line in lines:
        answers_Sent.append(line)
        
question_Count=0
option_Count=0
true_count = 0
same_Count=0
wrong_Count=0
while question_Count<501:
    try:
        predicted_Prob={}
        print('question no:',question_Count + 1)
        for questionWithOptions in questions_Sent[option_Count:option_Count+5]:
            questionWithOption=questionWithOptions.split('.')[1].strip()
            question_part1 = questionWithOption.split('[')[0]
            option = questionWithOption.split('[')[1].split(']')[0]
            question_part2 = questionWithOption.split('[')[1].split(']')[1].strip()
            question = question_part1 + question_part2
            question = question.replace('n\xe2\x80\x99t', ' not')
#             print(question, option)
            for word in question.strip().split(' '):
                if word.lower() not in stop_Word_List:
                    word=word.replace(',','')
                    option_Cosine_Similarity=cosine_Similarity_Words(word,option,question_Count)
                    predicted_Prob[word+'_'+option]=option_Cosine_Similarity                
        print predicted_Prob
        max_Prob = max(predicted_Prob.values())
#         print max_Prob
        count=0
        for prob in predicted_Prob.values():
            if prob==max_Prob:
                count+=1
        if(count>1):
            same_Count=same_Count+1
            print 'all same'
        else:
            for word_option, prob in predicted_Prob.items():
                if prob == max_Prob:
                    option = word_option.split('_')[1]
                    if option in answers_Sent[question_Count]:
                        print 'true', option
                        true_count += 1
                    else:
                        wrong_Count=wrong_Count+1
                        print 'wrong', option
        print('---------------------------------------------')
        question_Count=question_Count+1
        option_Count=option_Count+5
        print(true_count)
    except:
        print('exception occured')
        question_Count=question_Count+1
        option_Count=option_Count+5
        pass
    
print true_count
print same_Count
print wrong_Count
print broken_Words