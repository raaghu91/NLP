from nltk.corpus import wordnet
from itertools import product
from requests import get
from scipy import spatial
from nltk.corpus import stopwords
from gensim.models import Word2Vec
import os

word_line_no={}
line_offset = []

#Download data from http://deeptutor2.memphis.edu/Semilar-Web/public/lsa-models-lrec2014.html
#Merge all the lsaModel files and voc files
#cat wiki1/lsa_model1 wiki2/lsa_model2... > merged_lsaModel

def prepare_Data():
    fp1 = open("wiki_lsa_model/merged_voc")
    for i,word in enumerate(fp1):
        if word.strip() in word_line_no:
            continue
        word_line_no[word.strip()] = i
    offset = 0
    fp2 = open("wiki_lsa_model/merged_lsaModel")
    for line in fp2:
        line_offset.append(offset)
        offset += len(line)


prepare_Data()
# print word_line_no
# exit()

broken_Words={}
# prepare_Data()
# model=Word2Vec(wiki_Data_List, min_count=1)

def cosine_Similarity_Words(word, option, question_Count):
    try:
        fp = open("wiki_lsa_model/merged_lsaModel")
        fp.seek(line_offset[word_line_no[word]])
        vec1 = fp.readline()
        fp.seek(line_offset[word_line_no[option]])
        vec2 = fp.readline()
        vec1 = vec1.split()
        vec1 = map(float,vec1)
        vec2 = vec2.split()
        vec2 = map(float,vec2)
        result = 1 - spatial.distance.cosine(vec1, vec2)
        return result
    except:
        print 'Exception'
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((word, option))
        return 0.0
        

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

results_vector = open('Results/F7/F7_1_Output_Vector.txt','w+')
results_output= open('Results/F7/F7_1_Results.txt','w+')

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
#             print(question, option)
                
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
            print 'same'
            result = 'same'
        else:
            for word_option, prob in predicted_Prob.items():
                if prob == max_Prob:
                    option = word_option.split('_')[1]
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
    
print true_count
print same_Count
print wrong_Count
print broken_Words