import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import CFG
from nltk.parse import ChartParser, DependencyGraph
from natasha import  Segmenter, NewsEmbedding, NewsSyntaxParser,  Doc,  MorphVocab

grammar = CFG.fromstring("""
    S -> NP VP | VP
    NP -> Det N | N | N PP | Det N PP | Adj N
    VP -> V NP | V NP PP | V Adv | V Adj | V PP
    PP -> P NP
    Det -> 'этот' | 'тот' | 'его' | 'её' | 'их' | 'этой' | 'только' | 'что'
    N -> 'шум' | 'стройки' | 'процесс' | 'бетона' | 'балки' | 'здание' | 'организма' | 'кирпичи' | 'лучи' | 'солнца' | 'поверхности'
    V -> 'был' | 'скользили' | 'таская' | 'обретают' | 'наполнен' | 'сновали' | 'появились' | 'скользить' | 'залитого'
    P -> 'по' | 'на' | 'с' | 'в' | 'когда'
    Adj -> 'великолепный' | 'свежий' | 'большой' | 'маленький' | 'вечернего' | 'лениво' | 'залитого'
    Adv -> 'повсюду' | 'постепенно' | 'снова' | 'быстро' | 'лениво'
    Conj -> 'когда'
    Punc -> ',' | '.'
""")
parser = ChartParser(grammar)


segmenter = Segmenter()
embedding = NewsEmbedding()
syntax_parser = NewsSyntaxParser(embedding)
morph_vocab = MorphVocab()

with open('dataset.txt', 'r', encoding='utf-8') as file:
    dataset = file.read()


with open('output_lab3.txt', 'w+', encoding='utf-8') as output_file:
 
    paragraphs = [x for x in dataset.split('\n') if x != ""]
    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph)
        output_file.write('\tАбзац:\n')

        for sentence in sentences:
            output_file.write(f'Исходное предложение: {sentence}\n')

            words = word_tokenize(sentence)
            filtered_words = [x.lower() for x in words]
            output_file.write(f'Токенизированное предложение: {" ".join(filtered_words)}\n')

            try:
                trees = parser.chart_parse(filtered_words)
              

              
                output_file.write("Дерево NLTK:\n")
                for t in trees:
                    output_file.write(f'{t}\n')
                

            except Exception as e:
                output_file.write(f'Ошибка NLTK синтаксического анализа: {str(e)}\n')

            doc = Doc(sentence)
            doc.segment(segmenter)
          
            doc.parse_syntax(syntax_parser)

            output_file.write('Синтаксический анализ Natasha:\n')
            for sent in doc.sents:
                for token in sent.tokens:
                   
                    head_token = sent.tokens[int(token.head_id.split('_')[1]) - 1] if token.head_id != '0' else 'root'
                    head_text = head_token.text if token.head_id != '0' else 'root'
                    output_file.write(f'{token.text} -> {head_text} ({token.rel})\n')

        output_file.write('\n')
