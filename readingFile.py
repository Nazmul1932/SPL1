
from nltk.corpus import stopwords
import re
from collections import Counter

# load text
filename = "mozila.txt"
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
        # print(count)
        #for e in count:
         #  print(e, end=": ")
          # print(count[e])
        copy = []
        for k,v in count.items():
            copy.append((v, k))

        copy = sorted(copy, reverse = True)
        for k in copy:
            print('%s %d'%(k[1], k[0]))
    break



