with open("words.txt") as f:
    w1, w2 = f.readline().split()
    text = f.read()
    print(
        f"{w1} - {text.count(w1)}, {w2} - {text.count(w2)}\n drug za drugom: {text.count(w1+ " " +w2)+text.count(w2+ " " +w1)}"
    )
