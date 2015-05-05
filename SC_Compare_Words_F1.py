from nltk.corpus import wordnet
from itertools import product
from requests import get
from nltk.corpus import stopwords
# from PyDictionary import PyDictionary
# dictionary=PyDictionary()
# 
# print (dictionary.antonym("Life"))
# exit()

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
broken_Words={}
def compareWords(word1, word2, question_Count):
    try:
        ss1 = wordnet.synsets(word1)
        ss2 = wordnet.synsets(word2)
        return max(s1.path_similarity(s2) for (s1, s2) in product(ss1, ss2))
    except:
        print 'Exception'
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((word, option))
        return 0

#Get the stop word list from NLTK corpus
stop_Word_List = set(stopwords.words('english'))

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
                    option_Prob=compareWords(word,option, question_Count)
                    predicted_Prob[word+'_'+option]=option_Prob                
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
    except:
        print('exception occured')
        question_Count=question_Count+1
        option_Count=option_Count+5
        pass
    
print true_count
print same_Count
print wrong_Count
print broken_Words


