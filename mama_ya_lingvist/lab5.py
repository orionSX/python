import spacy
import networkx as nx
import matplotlib.pyplot as plt

nlp = spacy.load("ru_core_news_sm")
with open('dataset.txt', 'r', encoding='utf-8') as file:
    text = file.read()
doc = nlp(text)
def build_semantic_graph(sentence):
    G = nx.Graph()
    for token in sentence:
        G.add_node(token.text, pos=token.pos_, lemma=token.lemma_)
        for child in token.children:
            G.add_edge(token.text, child.text, label=f"{token.dep_} ({child.dep_})")
    return G
for i, sentence in enumerate(doc.sents):
    if i >= 5:
        break
    graph = build_semantic_graph(sentence)
    print(sentence)
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)  # Определяем расположение узлов
    nx.draw(graph, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    plt.title(f'Семантическая схема для: "{sentence.text}"', fontsize=14)
    plt.axis('off')
    plt.show()
