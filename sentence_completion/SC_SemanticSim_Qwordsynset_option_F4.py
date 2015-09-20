from nltk.corpus import wordnet
from itertools import product
from requests import get
from nltk.corpus import stopwords

# word="mother's"
# synsets = wordnet.synsets(word)
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

stop_Word_List = set(stopwords.words('english'))
    
#Feature 3
url = "http://swoogle.umbc.edu/StsService/GetStsSim"

#Text similarity
broken_Words={}
def sem_text_sim(s1, s2):
    try:
        response = get(url, params={'operation':'api','phrase1':s1,'phrase2':s2})
        return float(response.text.strip())
    except:
#         print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        print 'Exception'
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((s1, s2))
        return 0.0

# print sem_text_sim('movie','verbosity')
# exit()

results_vector = open('Results/F4/F4_1_Output_Vector.txt','w+')
results_output= open('Results/F4/F4_1_Results.txt','w+')

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
        
        sum_weights=0
        question = question.replace('n\xe2\x80\x99t', ' not')
        results_vector.write(str(question_Count+1));
        results_vector.write("\t");
        for option in option_List: 
            #find the probability for each synset and find the max_prob for all synsets for that option and store that in predicted_Prob
            for word in question.strip().split(' '):
                if word.lower() not in stop_Word_List:
                    word=word.replace(',','')
                    max_Synset_Prob=0
                    try:
                        synsets = wordnet.synsets(word)
                    except:
                        print 'Invalid word'
                    for synset in synsets:
                        curr_Synset_Prob=sem_text_sim(synset.definition(),option)
                        if curr_Synset_Prob>max_Synset_Prob:
                            max_Synset_Prob=curr_Synset_Prob
                    if option not in predicted_Prob.keys():
                            predicted_Prob[option]= max_Synset_Prob
                    else:
                        predicted_Prob[option]=predicted_Prob[option]+max_Synset_Prob
            results_vector.write(str(predicted_Prob[option]))
            results_vector.write("\t");
        
        results_vector.write("\n");  
        print predicted_Prob
        max_Prob = max(predicted_Prob.values())
        count=0
        for prob in predicted_Prob.values():
            if prob==max_Prob:
                count+=1
        result = ''
        if(count>1):
            same_Count=same_Count+1
            result='same'
            print 'same'
        else:
            for option, prob in predicted_Prob.items():
                if prob == max_Prob:
                    if option in answers_Sent[question_Count]:
                        print 'true', option
                        true_count += 1
                        result='yes'
                    else:
                        print 'wrong', option
                        wrong_Count=wrong_Count+1
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