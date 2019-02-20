
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
        result: str = ''.join(j for j in text if not j.isdigit())
        word = result.split()
        count = Counter(word)
        print(count)
        break



