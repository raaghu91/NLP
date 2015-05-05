f1_Results= open('Results/F1/F1_1_Results.txt','r')
f1_predictions = f1_Results.readlines()
f2_Results= open('Results/F2/F2_1_Results.txt','r')
f2_predictions = f2_Results.readlines()
f3_Results= open('Results/F3/F3_1_Results.txt','r')
f3_predictions = f3_Results.readlines()
f4_Results= open('Results/F4/F4_1_Results.txt','r')
f4_predictions = f4_Results.readlines()
f5_Results= open('Results/F5/F5_1_Results.txt','r')
f5_predictions = f5_Results.readlines()
# f6_Results= open('Results/F6/F6_1_Results.txt','r')
# f6_predictions = f6_Results.readlines()

all_features_Results= open('Results/Sink/results.txt','w+')

true_Count=0
false_Count=0
for i in range(0,501):
    print str(i+1)
    f1_q1=f1_predictions[i].split('.')[1].strip()
    print f1_q1
    f2_q1=f2_predictions[i].split('.')[1].strip()
    print f2_q1 
    f3_q1=f3_predictions[i].split('.')[1].strip()
    print f3_q1 
    f4_q1=f4_predictions[i].split('.')[1].strip()
    print f4_q1 
    f5_q1=f5_predictions[i].split('.')[1].strip()
    print f5_q1
    print '---------------------------------' 
#     f6_q1=f6_predictions[i].split('.')[1].strip() 
    all_features_Results.write(str(i+1) + ".")
    all_features_Results.write(f1_q1)
    all_features_Results.write('\t')
    all_features_Results.write(f2_q1)
    all_features_Results.write('\t')
    all_features_Results.write(f3_q1)
    all_features_Results.write('\t')
    all_features_Results.write(f4_q1)
    all_features_Results.write('\t')
    all_features_Results.write(f5_q1)
#     all_features_Results.write('\t')
#     all_features_Results.write(f6_q1)
    all_features_Results.write('\n')
    
#     if f1_q1 == 'yes' or f2_q1 == 'yes' or f3_q1 == 'yes' or f4_q1 == 'yes' or f5_q1 == 'yes' or f6_q1 == 'yes':
    if f1_q1 == 'yes' or f2_q1 == 'yes' or f3_q1 == 'yes' or f4_q1 == 'yes' or f5_q1 == 'yes':
        true_Count=true_Count+1
    else:
        false_Count=false_Count+1
         

print true_Count
print false_Count
print float(true_Count)/float(true_Count+false_Count)




