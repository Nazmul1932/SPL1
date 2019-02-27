
from nltk.corpus import stopwords
import re
from collections import Counter

# load text
filename = "gcc.txt"
file = open(filename, 'rt')
text = file.read()
file.close()

# split based on words only
words = re.split(r'\W+', text)
# print(words[:])

stopwords = stopwords.words('english')
stop_words = set(stopwords)

for i in words:
    if not i in stop_words:
        # print(i)
        result = ''.join(j for j in text if not j.isdigit())
        word = result.split()
        count = Counter(word)
        for e in count:
           print(e, end=": ")
           print(count[e])
           #print(count)
        break



