


from nltk.corpus import stopwords
import re
from collections import Counter

stop_words = set(stopwords.words('english'))


# load text
filename = 'mozila.txt'
file = open(filename, 'rt')
text = file.read()
file.close()


# split based on words only
words = re.split(r'\W+', text)
#print(words[:])

for i in words:
   if not i in stop_words:
      #print(i)
      print(Counter(text.split()))
      break

