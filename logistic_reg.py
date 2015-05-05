__author__ = 'raghu'

import numpy as np
import pandas as pd
from sklearn import datasets
import statsmodels.api as sm
from patsy import dmatrices
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score


def merge_results():
    f1_Results= open('Results/F1/F1_1_Output_Vector.txt','r')
    f1_predictions = f1_Results.readlines()
    f2_Results= open('Results/F2/F2_1_Output_Vector.txt','r')
    f2_predictions = f2_Results.readlines()
    f3_Results= open('Results/F3/F3_1_Output_Vector.txt','r')
    f3_predictions = f3_Results.readlines()
    f4_Results= open('Results/F4/F4_1_Output_Vector.txt','r')
    f4_predictions = f4_Results.readlines()
    f5_Results= open('Results/F5/F5_1_Output_Vector.txt','r')
    f5_predictions = f5_Results.readlines()
    f6_Results= open('Results/F6/F6_1_Output_Vector.txt','r')
    f6_predictions = f6_Results.readlines()
    f7_Results= open('Results/F7/F7_1_Output_Vector.txt','r')
    f7_predictions = f7_Results.readlines()
    answer_file = open('SC_answers.txt','r')
    answer_lines = answer_file.readlines()

    all_features_Results= open('logistic_reg_data.csv','w+')

    true_Count=0
    false_Count=0
    char_int_map = {'a':'1','b':'2', 'c':'3', 'd':'4', 'e':'5'}
    all_features_Results.write('answer,f1_1,f1_2,f1_3,f1_4,f1_5,f2_1,f2_2,f2_3,f2_4,f2_5,f3_1,f3_2,f3_3,f3_4,f3_5,f4_1,f4_2,f4_3,f4_4,f4_5,f5_1,f5_2,f5_3,f5_4,f5_5,f6_1,f6_2,f6_3,f6_4,f6_5,f7_1,f7_2,f7_3,f7_4,f7_5\n')
    # all_features_Results.write('answer,f1_1,f1_2,f1_3,f1_4,f1_5,f2_1,f2_2,f2_3,f2_4,f2_5,f3_1,f3_2,f3_3,f3_4,f3_5,f4_1,f4_2,f4_3,f4_4,f4_5,f5_1,f5_2,f5_3,f5_4,f5_5\n')
    for i in range(0,501):
        all_features_Results.write(char_int_map[answer_lines[i].split('.')[1].strip()])
        all_features_Results.write(",")
        f1_q1=f1_predictions[i].split('\t')[1:]
        if len(f1_q1) != 6:
            print('error1')
        all_features_Results.write(",".join(str(x).strip() for x in f1_q1))
        f2_q1=f2_predictions[i].split('\t')[1:]
        if len(f2_q1) != 6:
            print('error2')
        all_features_Results.write(",".join(str(x).strip() for x in f2_q1))
        f3_q1=f3_predictions[i].split('\t')[1:]
        if len(f3_q1) != 6:
            print('error3')
            print(i)
        all_features_Results.write(",".join(str(x).strip() for x in f3_q1))
        f4_q1=f4_predictions[i].split('\t')[1:]
        if len(f4_q1) != 6:
            print('error4')
        all_features_Results.write(",".join(str(x).strip() for x in f4_q1))
        f5_q1=f5_predictions[i].split('\t')[1:]
        if len(f5_q1) != 6:
            print('error5')
        all_features_Results.write(",".join(str(x).strip() for x in f5_q1))
        f6_q1=f6_predictions[i].split('\t')[1:]
        if len(f6_q1) != 6:
            print('error6')
            print(i)
        all_features_Results.write(",".join(str(x).strip() for x in f6_q1))
        f7_q1=f7_predictions[i].split('\t')[1:]
        if len(f7_q1) != 6:
            print('error7')
            print(i)
        # all_features_Results.write(",".join(str(x).strip() for x in f7_q1))
        text = ",".join(str(x).strip() for x in f7_q1)
        all_features_Results.write(text[:-1])
        all_features_Results.write("\n")
    #     print '---------------------------------'
    # #     f6_q1=f6_predictions[i].split('.')[1].strip()
    #     all_features_Results.write(str(i+1) + ".")
    #     all_features_Results.write(f1_q1)
    #     all_features_Results.write('\t')
    #     all_features_Results.write(f2_q1)
    #     all_features_Results.write('\t')
    #     all_features_Results.write(f3_q1)
    #     all_features_Results.write('\t')
    #     all_features_Results.write(f4_q1)
    #     all_features_Results.write('\t')
    #     all_features_Results.write(f5_q1)
    # #     all_features_Results.write('\t')
    #     all_features_Results.write(f6_q1)



merge_results()
# exit()
df = pd.read_csv("logistic_reg_data.csv")
# print df.columns
train_cols= X = df.columns[1:]
# y = df['answer']

# print(y)


y, X = dmatrices('answer ~ f1_1 + f1_2 + f1_3 + f1_4 + f1_5 + f2_1 + f2_2 + f2_3 + f2_4 + f2_5 + f3_1 + f3_2 + f3_3 + f3_4 + f3_5 + f4_1 + f4_2 + f4_3 + f4_4 + f4_5 + f5_1 + f5_2 + f5_3 + f5_4 + f5_5 + f6_1 + f6_2 + f6_3 + f6_4 + f6_5 + f7_1 + f7_2 + f7_3 + f7_4 + f7_5', df, return_type="dataframe")
# y, X = dmatrices('answer ~ f1_1 + f1_2 + f1_3 + f1_4 + f1_5 + f2_1 + f2_2 + f2_3 + f2_4 + f2_5 + f3_1 + f3_2 + f3_3 + f3_4 + f3_5 + f4_1 + f4_2 + f4_3 + f4_4 + f4_5 + f5_1 + f5_2 + f5_3 + f5_4 + f5_5', df, return_type="dataframe")
# model = LogisticRegression()
# model = model.fit(X, y)
# print(X)
y = np.ravel(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.3, random_state=0)
# print(X_train)
# print(X_test)
model = LogisticRegression()
model.fit(X_train, y_train)
print model.score(X_train, y_train)

# predict class labels for the test set
predicted = model.predict(X_test)
print predicted
count = 0
with open('logistic_reg_data.csv', 'r') as answer_file:
    for i,line in enumerate(answer_file):
        if i > 350:
            print(i,int(predicted[i-351]), line.split(',')[0])
            if int(predicted[i-351]) == int(line.split(',')[0]):
                count += 1
print(count,float(count)/151)

print metrics.accuracy_score(y_test, predicted)

# generate class probabilities
probs = model.predict_proba(X_test)
print len(probs)

