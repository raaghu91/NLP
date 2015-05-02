import urllib2
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re
import Queue
import socket

#this sets the default encoding to utf-8. the train_set contains characters which are not ASCII. So setting the default encoding to "utf-8"
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

visited_links={}
broken_links={}
visited_links_wikiDict={}
broken_links_wikiDict={}
wiki_Link = "http://en.wikipedia.org/wiki/"
wiki_dict="http://en.wiktionary.org/wiki/"


stop_Word_List = set(stopwords.words('english'))
stop_Word_List.add('!')
stop_Word_List.add(';')

def extractData(url,word):
    response = urllib2.urlopen(url)
    html = response.read() 
    soup = BeautifulSoup(html)
    wiki_Body = soup.findAll('div', {'class': 'mw-content-ltr'})
    file_Path = "wikiData/" + word +".txt"
    print file_Path
    f = open(file_Path, 'w')
    for p in wiki_Body:
        f.write(p.text.replace("\n"," "))

def extractWiki(question_Count, word):
    if word.lower() not in stop_Word_List:
        word=word.replace(',','')
#         if 'ed' in word[-2:]:
#             word=word[:-2]
        if 'ing' in word[-3:]:
            word=word[0:-3]
        try:
            if word not in visited_links:
                wiki_url = wiki_Link + word
                extractData(wiki_url,word)
                visited_links.setdefault(question_Count,[])
                visited_links[question_Count].append(word)
        except:
            print 'exception'
            broken_links.setdefault(question_Count,[])
            broken_links[question_Count].append(word)
            try:
                wikiDict_url=wiki_dict+word
                extractData(wikiDict_url,word)
                visited_links_wikiDict.setdefault(question_Count,[])
                visited_links_wikiDict[question_Count].append(word)
            except:
                broken_links_wikiDict.setdefault(question_Count,[])
                broken_links_wikiDict[question_Count].append(word)
                                
questions_Sent=[]
with open('SC_Final_Questions.txt','r') as questions_file:
    lines = questions_file.readlines()
    for line in lines:
        questions_Sent.append(line)
    
question_Count=425
option_Count=2115
while question_Count<501:
    print('question no:',question_Count + 1)
    question=''  
    for questionWithOptions in questions_Sent[option_Count:option_Count+5]:
        questionWithOption=questionWithOptions.split('.')[1].strip()
        if not question:
            question_part1 = questionWithOption.split('[')[0]
            question_part2 = questionWithOption.split('[')[1].split(']')[1].strip()
            question = question_part1 + question_part2
        option = questionWithOption.split('[')[1].split(']')[0]
        extractWiki(question_Count, option)
    for word in question.strip().split(' '):
        extractWiki(question_Count, word)
    question_Count=question_Count+1
    option_Count=option_Count+5
    print '---------------------------------------'
    
print visited_links
print broken_links
print visited_links_wikiDict
print broken_links_wikiDict