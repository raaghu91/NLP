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

wiki_Data_List=[]
def prepare_Data():
    dir="wikiData/"
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
        return model.similarity(word, option)#cos similarity between two words
    except:
        print 'Exception'
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((word, option))
        return 0.0
         
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


results_vector = open('Results/F5/F5_1_Output_Vector.txt','w+')
results_output= open('Results/F5/F5_1_Results.txt','w+')

question_Count=0
option_Count=0
true_count = 0
same_Count=0
wrong_Count=0
while question_Count<501:
    try:
        predicted_Prob={}
        print('question no:',question_Count + 1)
        question='' 
        option_List=[]
        for questionWithOptions in questions_Sent[option_Count:option_Count+5]:
            questionWithOption=questionWithOptions.split('.')[1].strip()
            if not question:
                question_part1 = questionWithOption.split('[')[0]
                question_part2 = questionWithOption.split('[')[1].split(']')[1].strip()
                question = question_part1 + question_part2
            option = questionWithOption.split('[')[1].split(']')[0]
            option_List.append(option) 
        question = question.replace('n\xe2\x80\x99t', ' not')
        results_vector.write(str(question_Count+1));
        results_vector.write("\t");
        
        for option in option_List: 
            for word in question.strip().split(' '):
                if word.lower() not in stop_Word_List:
                    word=word.replace(',','')
                    option_Cosine_Similarity=cosine_Similarity_Words(word,option,question_Count)
                    if option not in predicted_Prob.keys():
                        predicted_Prob[option]= option_Cosine_Similarity
                    else:
                        predicted_Prob[option]=predicted_Prob[option]+option_Cosine_Similarity
            results_vector.write(str(predicted_Prob[option]))
            results_vector.write("\t");
            
        results_vector.write("\n");          
        print predicted_Prob
        max_Prob = max(predicted_Prob.values())
#         print max_Prob
        count=0
        for prob in predicted_Prob.values():
            if prob==max_Prob:
                count+=1
        result = ''
        if(count>1):
            same_Count=same_Count+1
            result = 'same'
            print 'same'
        else:
            for option, prob in predicted_Prob.items():
                if prob == max_Prob:
                    if option in answers_Sent[question_Count]:
                        print 'true', option
                        true_count += 1
                        result = 'yes'
                    else:
                        wrong_Count=wrong_Count+1
                        print 'wrong', option
                        result = 'no'
        results_output.write(str(question_Count+1) + ". " + result);
        results_output.write("\n"); 
        print('---------------------------------------------')
        question_Count=question_Count+1
        option_Count=option_Count+5
        print(true_count)
    except:
        results_output.write(str(question_Count+1) + "Exception")
        results_output.write("\n");
        print('exception occured')
        question_Count=question_Count+1
        option_Count=option_Count+5
        pass

print '-------------------------' 
print true_count
print same_Count
print wrong_Count
print broken_Words