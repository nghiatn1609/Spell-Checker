import re
import glob
import os
from typing import Counter

words = []
for filename in glob.glob('C:/Users/Admin/Desktop/Spell Checker/datasetSpellChecker/*[0-9].txt'):
    with open(os.path.join(os.getcwd(), filename), 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in lines:
             words += re.findall(r'[a-zA-Z]+', line.lower())
WordCount = Counter(words)          
print(len(words))   
# with open("library.txt",'w') as f:
#     for i in words:
#         f.write(i)
#         f.write(",")
with open("CountWord.txt",'w+') as f:
    for i in words:
        f.write(i)
        f.write(": ")
        f.write(str(WordCount[i]))
        f.write("\n")
with open("CountWord.txt","r") as d:
    lines = d.readlines()
    line = list(set(lines))    
with open("CountWord.txt",'w+') as g:
    for i in line:
        g.write(i)

f.close()  
d.close()
g.close()      
