from nltk.corpus import wordnet
from itertools import product
from requests import get
from nltk.corpus import stopwords

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
        
#Feature 3
url = "http://swoogle.umbc.edu/StsService/GetStsSim"

#Text similarity
def sem_text_sim(s1, s2):
    try:
        response = get(url, params={'operation':'api','phrase1':s1,'phrase2':s2})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0
    
question_Count=0
option_Count=0
true_count = 0
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
            #find the probability for each synset and find the max_prob for all synsets for that option and store that in predicted_Prob
            max_Synset_Prob=0
            synsets = wordnet.synsets(option)
            for synset in synsets:
                curr_Synset_Prob=sem_text_sim(question,synset.definition())
                if curr_Synset_Prob>max_Synset_Prob:
                    max_Synset_Prob=curr_Synset_Prob
            predicted_Prob[option]=max_Synset_Prob
        
        print predicted_Prob
        max_Prob = max(predicted_Prob.values())
        count=0
        for prob in predicted_Prob.values():
            if prob==max_Prob:
                count+=1
        if(count>1):
            print 'all same'
        else:
            for option, prob in predicted_Prob.items():
                if prob == max_Prob:
                    if option in answers_Sent[question_Count]:
                        print 'true', option
                        true_count += 1
                    else:
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
  