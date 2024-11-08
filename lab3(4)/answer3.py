def ans(filename):
    with open(filename) as f:
        n, k, m = map(int, f.readline().split())

        matr = []
        for i in range(m):
            l, r, c, p = map(int, f.readline().split())
            temp = [0] * (n + 1)
            for t in range(l - 1, r):
                temp[t] = c
            temp[-1] = p
            matr.append(temp)
        matr.sort(key=lambda x: x[-1])
        price = 0

        for i in range(n):
            cores = k
            for x in matr:
                if x[i] != 0:
                    if x[i] >= cores:
                        price += cores * x[-1]
                        break
                    else:
                        cores -= x[i]
                        price += x[i] * x[-1]
                        x[i] = 0
                        continue

        return price


print(f"f1 - {ans('lasttask.txt')}")
print(f"f2 - {ans('lt2.txt')}")
print(f"f3 - {ans('lt3.txt')}")
