import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize

nltk.download('stopwords')
nltk.download('punkt_tab')
stop_words=stopwords.words('russian')
found_stop_words=[]
with open('dataset.txt', 'r', encoding='utf-8') as file:
    dataset = file.read()

tokenized=word_tokenize(dataset)
filtered=[x for x in tokenized if x.lower() not in stop_words]
found_stop_words=[x.lower() for x in tokenized if x.lower() in stop_words]

with open('output_stop_words_lab1.txt', 'w+',encoding='utf-8') as file:
    file.write(f'Всего в датасете было {len(found_stop_words)} стоп-слов, из них уникальных: {len(set(found_stop_words))}\n {set(found_stop_words)}')
with open('output_filtered_lab1.txt', 'w+',encoding='utf-8') as file:
    ar=[x for x in dataset.split('\n') if x !=""]
    for abz in ar:
        sents=sent_tokenize(abz)
        file.write('\t\t')
        for sent in sents:
            words=word_tokenize(sent)
            filtered_words=[x for x in words if x.lower() not in stop_words]
            s=" ".join(filtered_words)
            file.write(s+'\n')