def build_latin_english_dict(data):
 
    latin_to_english = {}

 
    for line in data:
        english_word, latin_words_str = line.split(' - ')
        latin_words = latin_words_str.split(', ')

        
        for latin_word in latin_words:
            if latin_word not in latin_to_english:
                latin_to_english[latin_word] = []
            latin_to_english[latin_word].append(english_word)

  
    sorted_latin_to_english = {}
    for latin_word in sorted(latin_to_english):
        sorted_latin_to_english[latin_word] = sorted(latin_to_english[latin_word])

    return sorted_latin_to_english



n = int(input('Enter number of en words: ')) 
data = [input('Enter word_dict : eng_word - x1, x2, x3 \n').strip() for _ in range(n)]


latin_to_english_dict = build_latin_english_dict(data)

print(len(latin_to_english_dict))
for latin_word, english_words in latin_to_english_dict.items():
    print(f"{latin_word} - {', '.join(english_words)}")
