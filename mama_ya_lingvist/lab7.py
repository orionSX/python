import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pymorphy3
import re
from nltk.tokenize import RegexpTokenizer
from functools import lru_cache


nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)


morph = pymorphy3.MorphAnalyzer()
stop_words = set(nltk.corpus.stopwords.words('russian'))
tokenizer = RegexpTokenizer(r'\w+')

@lru_cache(maxsize=10000)  
def lemmatize_word(word):
    return morph.parse(word)[0].normal_form

def preprocess_text(text):    
    text = re.sub(r'[^\w\s]', '', text).lower()
    tokens = tokenizer.tokenize(text)
    tokens = [token for token in tokens if token not in stop_words]
    lemmas = [lemmatize_word(token) for token in tokens]
    return " ".join(lemmas)

def fuzzy_semantic_classification(query, sentences):   
    if not query or not sentences:
        raise ValueError("Запрос и список предложений не должны быть пустыми.")
    
   
    preprocessed_query = preprocess_text(query)
    preprocessed_sentences = [preprocess_text(sentence) for sentence in sentences]
    
  
    documents = [preprocessed_query] + preprocessed_sentences
    vectorizer = TfidfVectorizer().fit(documents)
    tfidf_matrix = vectorizer.transform(documents)

   
    query_vector = tfidf_matrix[0]
    
    similarities = cosine_similarity(query_vector, tfidf_matrix[1:]).flatten()


    results = {
        sentence: similarity for sentence, similarity in zip(sentences, similarities)
    }
    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))


query = "программирование - процесс создания программного обеспечивания, который включает в себя применения алгоритмов для решения разных проблем"
sentences = [
    "Программирование — это процесс создания программ, которые управляют поведением вычислительных систем.",
    "Оно включает разработку алгоритмов и их реализацию с использованием различных языков программирования, таких как Python, Java, C++ и другие.",
    "Эффективное программирование требует понимания сложности алгоритмов, теории вычислений и принципов разработки программного обеспечения.",
    "Шум стройки был повсюду.",
    "Её применение особенно важно в компьютерных науках и теории алгоритмов, где дискретные объекты — например, целые числа, графы и логические операторы — играют ключевую роль в моделировании данных и разработке эффективных алгоритмов.",
    ]

try:
    results = fuzzy_semantic_classification(query, sentences)
    print(f"Запрос: '{query}'")
   
    for sentence, similarity in results.items():
        print(f"Предложение: '{sentence}' Степень сходства: {similarity:.2f}")
except ValueError as e:
    print(e)
