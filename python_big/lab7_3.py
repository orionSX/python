c = [
    [14, 5, 27, 29, 23],
    [17, 7, 16, 19, 2],
    [20, 12, 15, 29, 5],
    [14, 24, 18, 7, 13]
]
a = [18, 14, 16, 12]
b = [8, 11, 11, 9, 21]

c_zero = [[0 for _ in range(5)] for _ in range(4)]
c_true = [[True for _ in range(5)] for _ in range(4)]

if sum(a) == sum(b):
    print("The problem is closed because sum(a) == sum(b)")
else:
    print("The problem is not closed because sum(a) != sum(b)")
print("")

def min_element(c, c_true):
    minimum = float('inf')
    ind1, ind2 = 0, 0
    for i in range(len(c)):
        for j in range(len(c[0])):
            if c_true[i][j] and c[i][j] <= minimum:
                minimum = c[i][j]
                ind1, ind2 = i, j
    return ind1, ind2

def plan(c, c_zero, c_true, a, b):
    count = 0
    while sum(a) + sum(b) > 0:
        count += 1
        ind1, ind2 = min_element(c, c_true)
        if a[ind1] >= b[ind2]:
            a[ind1] -= b[ind2]
            c_zero[ind1][ind2] = b[ind2]
            b[ind2] = 0
            for i in range(len(c)):
                c_true[i][ind2] = False
        else:
            b[ind2] -= a[ind1]
            c_zero[ind1][ind2] = a[ind1]
            a[ind1] = 0
            for j in range(len(c[0])):
                c_true[ind1][j] = False

    v = len(c) + len(c[0]) - 1 == count
    if v:
        print("The initial plan is degenerate because m + n - 1 = number of basic elements.")
    else:
        print("The initial plan is non-degenerate because m + n - 1 != number of basic elements.")
    print("")

    total_cost = 0
    for i in range(len(c)):
        for j in range(len(c[0])):
            total_cost += c_zero[i][j] * c[i][j]

    print(f"Total costs: {total_cost}")
    print("")
    return c_zero

def potentials(c_zero, c):
    u = [None] * len(c)
    v = [None] * len(c[0])
    u[0] = 0
    while True:
        for i in range(len(c)):
            for j in range(len(c[0])):
                if c_zero[i][j] != 0:
                    if u[i] is None and v[j] is None:
                        continue
                    elif u[i] is None:
                        u[i] = c[i][j] - v[j]
                    else:
                        v[j] = c[i][j] - u[i]
        if all(x is not None for x in u) and all(x is not None for x in v):
            break
    return u, v

def check_optimality(c_zero, c, u, v):
    negative = []
    for i in range(len(c)):
        for j in range(len(c[0])):
            if c_zero[i][j] == 0 and c[i][j] < u[i] + v[j]:
                delta = c[i][j] - (u[i] + v[j])
                negative.append((delta, i, j))

    if not negative:
        print("The plan is optimal.")
        print("")
        return None, None
    else:
        print("The plan is not optimal.")
        print("")
        return min(negative, key=lambda x: x[0])[1:]

def find_cycle(c_zero, ind1, ind2):
    visited = [[False for _ in range(len(c_zero[0]))] for _ in range(len(c_zero))]
    path = []
    visited[ind1][ind2] = True
    current_sign = "+"

    def dfs(x, y, direction):
        nonlocal current_sign
        for i in range(len(c_zero)):
            for j in range(len(c_zero[0])):
                if direction == 'row' and i != x: continue
                if direction == 'col' and j != y: continue

                if c_zero[i][j] != 0 and not visited[i][j]:
                    current_sign = "-" if current_sign == "+" else "+"
                    path.append((current_sign, i, j, c_zero[i][j]))
                    visited[i][j] = True

                    if direction == 'row':
                        if dfs(i, j, 'col'):
                            return True
                    else:
                        if dfs(i, j, 'row'):
                            return True

                    path.pop()
                    visited[i][j] = False
                    current_sign = "-" if current_sign == "+" else "+"
                elif (i, j) == path[0][1:3] and len(path) > 2:
                    return True

        return False

    path.append((current_sign, ind1, ind2, c_zero[ind1][ind2]))
    dfs(ind1, ind2, 'row')
    return path if len(path) > 2 else []

def find_min_in_cycle(cycle):
    negative_elements = [x for x in cycle if x[0] == '-' and x[3] != 0]
    return min(negative_elements, key=lambda x: x[3]) if negative_elements else None

def update_cycle(c_zero, cycle):
    min_value_tuple = find_min_in_cycle(cycle)
    min_value = min_value_tuple[3]
    print(f"Minimum value for updating the cycle: {min_value}")
    print("")

    for sign, i, j, _ in cycle:
        if sign == '+':
            c_zero[i][j] += min_value
        elif sign == '-':
            c_zero[i][j] -= min_value

    return c_zero

def method(c_zero, c_true, c, a, b):
    c_zero = plan(c, c_zero, c_true, a.copy(), b.copy())

    while True:
        u, v = potentials(c_zero, c)
        ind1, ind2 = check_optimality(c_zero, c, u, v)
        if ind1 is None and ind2 is None:
            break
        cycle = find_cycle(c_zero, ind1, ind2)
        c_zero = update_cycle(c_zero, cycle)
        print(f"Cycle: {cycle}\nUpdated plan:")
        for row in c_zero:
            print(row)

    print("\nFinal plan:")
    for row in c_zero:
        print(row)
    print("")
    total_cost = sum(c_zero[i][j] * c[i][j] for i in range(len(c)) for j in range(len(c[0])))
    print(f"Total costs: {total_cost}")

method(c_zero, c_true, c, a, b)
