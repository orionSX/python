import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.stem import SnowballStemmer

nltk.download('stopwords')
nltk.download('punkt_tab')
stop_words=stopwords.words('russian')
stemmer = SnowballStemmer("russian")
with open('dataset.txt', 'r', encoding='utf-8') as file:
    dataset = file.read()

with open('output_stemmed_lab2.txt', 'w+',encoding='utf-8') as file:
    ar=[x for x in dataset.split('\n') if x !=""]
    for abz in ar:
        sents=sent_tokenize(abz)
        file.write('\t')
        for sent in sents:
            words=word_tokenize(sent)
            filtered_words=[x for x in words if x.lower() not in stop_words]
            stemmed_words=[stemmer.stem(x) for x in filtered_words]
            s=" ".join(stemmed_words)
            file.write(s+'\n')