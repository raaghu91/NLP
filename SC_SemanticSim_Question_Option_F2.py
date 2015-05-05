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
        
#Feature 2
url = "http://swoogle.umbc.edu/StsService/GetStsSim"

#Text similarity
broken_Words={}
def sem_text_sim(s1, s2):
    try:
        response = get(url, params={'operation':'api','phrase1':s1,'phrase2':s2})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        broken_Words.setdefault(question_Count,[])
        broken_Words[question_Count].append((word, option))
        return 0.0


results_vector = open('Results/F2/F2_1_Output_Vector.txt','w+')
results_output= open('Results/F2/F2_1_Results.txt','w+')

question_Count=0
option_Count=0
true_count = 0
same_Count=0
wrong_Count=0
while question_Count<501:
    try:
        predicted_Prob={}
        print('question no:',question_Count + 1)
        results_vector.write(str(question_Count+1));
        results_vector.write("\t");
        for questionWithOptions in questions_Sent[option_Count:option_Count+5]:
            questionWithOption=questionWithOptions.split('.')[1].strip()
            question_part1 = questionWithOption.split('[')[0]
            option = questionWithOption.split('[')[1].split(']')[0]
            question_part2 = questionWithOption.split('[')[1].split(']')[1].strip()
            question = question_part1 + question_part2
#                 print(question, option)
            option_Prob=sem_text_sim(question,option)
            predicted_Prob[option]=option_Prob
            
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