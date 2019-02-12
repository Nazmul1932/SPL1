


#mozila.txt
#eclipse.txt


import io
from nltk.corpus import stopwords
import re

stop_words = set(stopwords.words('english'))
# load text


filename = 'mozila.txt'
file = open(filename, 'rt')
text = file.read()
file.close()

# split based on words only
words = re.split(r'\W+', text)
print(words[:])

for r in words:
   if not r in stop_words:
      print(r)



