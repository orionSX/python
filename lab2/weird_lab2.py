def guess_number(n, questions):
    possible_numbers = set(range(1, n + 1))  
    answers = []

    for question in questions:
        if question == "HELP":
            break
        numbers = set(map(int, question.split()))
        
        
        if len(numbers) > len(possible_numbers) / 2:
            
            answers.append("YES")
            possible_numbers.intersection_update(numbers)
        else:
           
            answers.append("NO")
            possible_numbers.difference_update(numbers)

    return answers, sorted(possible_numbers)



n = int(input('Enter n: ')) 
questions = []
while True:
    question = input('Enter Arr\n').strip()
    if question == "HELP":
        break
    questions.append(question)


answers, remaining_numbers = guess_number(n, questions)

for answer in answers:
    print(answer)


print(" ".join(map(str, remaining_numbers)))
