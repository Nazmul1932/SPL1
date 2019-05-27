from nltk.corpus import stopwords
import re
from collections import Counter



filename = "mozila.txt"
file = open(filename, 'rt')
text = file.read()
file.close()

words = re.split(r'\W+', text)

stopwords = stopwords.words('english')
stop_words = set(stopwords)

for i in words:
    if not i in stop_words:

        result = ''.join(j for j in text if not j.isdigit())
        word = result.split()
        count = Counter(word)
        len_of_dataset = len(count)
       

        column = []
        for k, word in enumerate(sorted(count, key=count.get, reverse=True)[:500]):
            column = (count[word])
            #print('%s-%s' % (word,count[word]))
            matrix = [14019][500]
            for l in range(14019):
                for m in range(500):
                    

    break
