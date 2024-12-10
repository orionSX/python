from sentence_transformers import SentenceTransformer, util
import spacy


model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

with open('dataset.txt', 'r', encoding='utf-8') as file:
    text = file.read()

nlp = spacy.load("ru_core_news_sm")
doc = nlp(text)

sentences = [sent.text for sent in list(doc.sents)[:5]]


sentence_embeddings = model.encode(sentences)


print("Семантическая близость между предложениями (на основе векторных представлений):")
for i in range(len(sentences)):
    for j in range(i + 1, len(sentences)):
        similarity = util.cos_sim(sentence_embeddings[i], sentence_embeddings[j]).item()
        print(f"Схожесть между предложением {i+1} и {j+1}: {similarity:.2f}")

print("\nСравниваемые предложения:")
for i, sentence in enumerate(sentences):
    print(f"{i+1}: {sentence}")
