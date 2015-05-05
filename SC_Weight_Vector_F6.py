from nltk.corpus import wordnet
from itertools import product
from requests import get
from nltk.corpus import stopwords
import os
import math

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
 
#Feature 1
def compareWords(word1, word2):
    ss1 = wordnet.synsets(word1)
    ss2 = wordnet.synsets(word2)
    return max(s1.path_similarity(s2) for (s1, s2) in product(ss1, ss2))

wiki_Data_List={}
def prepare_Data():
    dir="wikiData/"
    files = os.listdir(dir)
    for fname in files:
        with open(dir+fname) as infile:
            file_Data=infile.read()
            sentences=file_Data.split('.')
            wiki_Data_List.setdefault(fname,[])
            file_Sents=[]
            for sentence in sentences:
                word_List=[word for word in sentence.strip(' ').split(' ') if word != ' ']
                file_Sents.append(word_List)
            wiki_Data_List[fname]=file_Sents
          
def computeIDF(word):
#     print wiki_Data_List
    doc_Freq=0
    for file, sents in wiki_Data_List.items():
        for sent in sents:
            if word in sent:
                doc_Freq=doc_Freq+1
                break
    numDocs=len(wiki_Data_List.keys())
#     print word, numDocs, doc_Freq
    if doc_Freq!=0:
        return math.log(float(numDocs)/float(doc_Freq))
    else:
        return 0


#execution
# prepare_Data()
# computeIDF('form')
# exit()

weight_Vector={}
broken_Words={}
def similarityScore_Weights(word,option,question_Count):
    try:
#         print word, option
        weight_Word=0
        weight_Option=0
        if word not in weight_Vector:
            weight_Word = computeIDF(word)
            weight_Vector[word]=weight_Word
        else:
            weight_Word=weight_Vector[word]
        
        if option not in weight_Vector:
            weight_Option = computeIDF(option)
            weight_Vector[option]=weight_Option
        else:
            weight_Option=weight_Vector[option]
            
        word_Similarity = compareWords(word, option)
#         print weight_Word, word_Similarity
        return word_Similarity*weight_Option*weight_Word
    except:
#         print 'Exception'
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((word, option))
        return 0
    
#Get the stop word list from NLTK corpus
stop_Word_List = set(stopwords.words('english'))

results_vector = open('Results/F6/F6_1_Output_Vector.txt','w+')
results_output= open('Results/F6/F6_1_Results.txt','w+')

question_Count=0
option_Count=0
true_count = 0
same_Count=0
wrong_Count=0
prepare_Data()
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
#             print(question, option)
        results_vector.write(str(question_Count+1));
        results_vector.write("\t");
        
        sum_weights=0
        for option in option_List: 
            for word in question.strip().split(' '):
                if word.lower() not in stop_Word_List:
                    word=word.replace(',','')
                    option_Prob=similarityScore_Weights(word,option,question_Count)
                    if option not in predicted_Prob.keys():
                        predicted_Prob[option]= option_Prob
                    else:
                        predicted_Prob[option]=predicted_Prob[option]+option_Prob
                    sum_weights= sum_weights+weight_Vector[word]
            predicted_Prob[option]=predicted_Prob[option]/sum_weights
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
        result=''
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
      
print true_count
print same_Count
print wrong_Count
print broken_Words