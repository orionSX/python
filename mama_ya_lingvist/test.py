import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import CFG
from nltk.parse import ChartParser, DependencyGraph
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsSyntaxParser,
    Doc
)

grammar = CFG.fromstring("""
 S -> NP VP
 PP -> P NP
 NP -> Det N | Det N PP | 'I'
 VP -> V NP | VP PP
 Det -> 'an' | 'my'
 N -> 'elephant' | 'pajamas'
 V -> 'shot'
 P -> 'in'
 """)
sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
parser = nltk.ChartParser(grammar)
trees = parser.chart_parse(sent)
for tree in trees:
    print (tree)