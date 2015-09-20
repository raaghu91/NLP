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
    # f4_Results= open('Results/F4/F4_1_Output_Vector.txt','r')
    # f4_predictions = f4_Results.readlines()
    f5_Results= open('Results/F5/F5_1_Output_Vector.txt','r')
    f5_predictions = f5_Results.readlines()
    f6_Results= open('Results/F6/F6_1_Output_Vector.txt','r')
    f6_predictions = f6_Results.readlines()
    # f7_Results= open('Results/F7/F7_1_Output_Vector.txt','r')
    # f7_predictions = f7_Results.readlines()
    answer_file = open('SC_answers.txt','r')
    answer_lines = answer_file.readlines()

    all_features_Results= open('logistic_reg_data.csv','w+')

    true_Count=0
    false_Count=0
    f1_vector = []
    f2_vector = []
    f3_vector = []
    f5_vector = []
    f6_vector = []
    char_int_map = {'a':'1','b':'2', 'c':'3', 'd':'4', 'e':'5'}
    all_features_Results.write('answer,f1_1,f1_2,f1_3,f1_4,f1_5,f2_1,f2_2,f2_3,f2_4,f2_5,f3_1,f3_2,f3_3,f3_4,f3_5,f5_1,f5_2,f5_3,f5_4,f5_5,f6_1,f6_2,f6_3,f6_4,f6_5\n')
    # all_features_Results.write('answer,f1_1,f1_2,f1_3,f1_4,f1_5,f2_1,f2_2,f2_3,f2_4,f2_5,f3_1,f3_2,f3_3,f3_4,f3_5,f4_1,f4_2,f4_3,f4_4,f4_5,f5_1,f5_2,f5_3,f5_4,f5_5\n')
    for i in range(0,501):
        # all_features_Results.write(char_int_map[answer_lines[i].split('.')[1].strip()])
        # all_features_Results.write(",")
        f1_q1=f1_predictions[i].split('\t')[1:]
        if len(f1_q1) != 6:
            print('error1')
        f1_q1.pop()
        for x in f1_q1:
            f1_vector.append(x)
        # print(len(f1_vector), len(f1_q1),f1_predictions[i],f1_vector)
        # all_features_Results.write(",".join(str(x).strip() for x in f1_q1))
        f2_q1=f2_predictions[i].split('\t')[1:]
        if len(f2_q1) != 6:
            print('error2')
        f2_q1.pop()
        for x in f2_q1:
            f2_vector.append(x)
        # all_features_Results.write(",".join(str(x).strip() for x in f2_q1))
        f3_q1=f3_predictions[i].split('\t')[1:]
        if len(f3_q1) != 6:
            print('error3')
            print(i)
        f3_q1.pop()
        for x in f3_q1:
            f3_vector.append(x)
        # all_features_Results.write(",".join(str(x).strip() for x in f3_q1))
        # f4_q1=f4_predictions[i].split('\t')[1:]
        # if len(f4_q1) != 6:
        #     print('error4')
        # all_features_Results.write(",".join(str(x).strip() for x in f4_q1))
        f5_q1=f5_predictions[i].split('\t')[1:]
        if len(f5_q1) != 6:
            print('error5')
        f5_q1.pop()
        for x in f5_q1:
            f5_vector.append(x)
        # all_features_Results.write(",".join(str(x).strip() for x in f5_q1))
        f6_q1=f6_predictions[i].split('\t')[1:]
        if len(f6_q1) != 6:
            print('error6')
            print(i)
        f6_q1.pop()
        for x in f6_q1:
            f6_vector.append(x)
        # all_features_Results.write(",".join(str(x).strip() for x in f6_q1))
        # f7_q1=f7_predictions[i].split('\t')[1:]
        # if len(f7_q1) != 6:
        #     print('error7')
        #     print(i)
        # all_features_Results.write(",".join(str(x).strip() for x in f7_q1))
        # text = ",".join(str(x).strip() for x in f6_q1)
        # all_features_Results.write(text[:-1])
        # all_features_Results.write("\n")

    def min_fn(vec):
        min=1000.0
        for x in vec:
            val=float(x)
            if val<min:
                min=val
        return min

    def max_fn(vec):
        max=0.0
        for x in vec:
            val=float(x)
            if val>max:
                max=val
        return max

    # f1_vector = [j for i in f1_vector for j in i]
    # f1_vec=[]
    # for x in f1_vector:
    #     f1_vec.append(float(x))
    # f1_vec = [j for i in f1_vec for j in i]
    # print len(f1_vector)
    # x_np = np.asarray(float(x) for x in f1_vector)

    f1_norm=[]
    min = min_fn(f1_vector)
    max=max_fn(f1_vector)
    for i,x in enumerate(f1_vector):
        x_np=float(x)
        val = (x_np - min) / (max - min)
        f1_norm.append(val)
    print(len(f1_norm))
    print(f1_norm)
    for i,x in enumerate(f1_norm):
        if x == 1:
            print('yessss', i)

    f2_norm=[]
    min = min_fn(f2_vector)
    max=max_fn(f2_vector)
    for i,x in enumerate(f2_vector):
        x_np=float(x)
        val = (x_np - min) / (max - min)
        f2_norm.append(val)

    f3_norm=[]
    min = min_fn(f3_vector)
    max=max_fn(f3_vector)
    for i,x in enumerate(f3_vector):
        x_np=float(x)
        val = (x_np - min) / (max - min)
        f3_norm.append(val)
    f5_norm=[]
    min = min_fn(f5_vector)
    max=max_fn(f5_vector)
    for i,x in enumerate(f5_vector):
        x_np=float(x)
        val = (x_np - min) / (max - min)
        f5_norm.append(val)

    f6_norm=[]
    min = min_fn(f6_vector)
    max=max_fn(f6_vector)
    for i,x in enumerate(f6_vector):
        x_np=float(x)
        val = (x_np - min) / (max - min)
        f6_norm.append(val)

    j = 0
    for i in range(0,501):
        all_features_Results.write(char_int_map[answer_lines[i].split('.')[1].strip()])
        all_features_Results.write(",")
        all_features_Results.write(",".join(str(x).strip() for x in f1_norm[j:j+5]))
        all_features_Results.write(",")
        all_features_Results.write(",".join(str(x).strip() for x in f2_norm[j:j+5]))
        all_features_Results.write(",")
        all_features_Results.write(",".join(str(x).strip() for x in f3_norm[j:j+5]))
        all_features_Results.write(",")
        all_features_Results.write(",".join(str(x).strip() for x in f5_norm[j:j+5]))
        all_features_Results.write(",")
        all_features_Results.write(",".join(str(x).strip() for x in f6_norm[j:j+5]))
        j+=5
        all_features_Results.write("\n")



    # exit()
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


y, X = dmatrices('answer ~ f1_1 + f1_2 + f1_3 + f1_4 + f1_5 + f2_1 + f2_2 + f2_3 + f2_4 + f2_5 + f3_1 + f3_2 + f3_3 + f3_4 + f3_5 + f5_1 + f5_2 + f5_3 + f5_4 + f5_5 + f6_1 + f6_2 + f6_3 + f6_4 + f6_5', df, return_type="dataframe")
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

