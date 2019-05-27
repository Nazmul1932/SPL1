from nltk.corpus import stopwords
import re
from collections import Counter
from nltk.stem import PorterStemmer




filename = "mozila.txt"
file = open(filename, 'rt')
text = file.read()
file.close()

words = re.split(r'\W+', text)

stopwords = stopwords.words('english')
stop_words = set(stopwords)

ps = PorterStemmer()




for i in words:
    for w in stop_words:
        stem_words = ps.stem(w)

    if not i in stem_words:

        result = ''.join(j for j in text if not j.isdigit())
        word = result.split()
        count = Counter(word)

        column = []
        for k, word in enumerate(sorted(count, key=count.get, reverse=True)[:500]):
            column = (count[word])
            print(column, end = ' ,')

    break





'''
data = []
            feature_word = [word]
            #print(len(feature_word)
            for line in len_of_dataset:
                arr = [0]*len(feature_word)
                #print(arr)
                index = 0
                for w in feature_word:
                    c = line.count(w)
                    arr[index] = c
                    index = index + 1
                data.append(arr)
    break
'''
