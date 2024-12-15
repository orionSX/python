def simplex_method(c, A, b):
    import numpy as np

    num_vars = len(c)
    num_constraints = len(b)

  
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:num_constraints, :num_vars] = A
    tableau[:num_constraints, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    tableau[:num_constraints, -1] = b
    tableau[-1, :num_vars] = -np.array(c)
    

   
    while np.any(tableau[-1, :-1] < 0):
        pivot_col = np.argmin(tableau[-1, :-1])

        if all(tableau[:-1, pivot_col] <= 0):
            raise ValueError("Optimal solution is unbounded!")

        ratios = np.divide(
            tableau[:-1, -1], tableau[:-1, pivot_col],
            out=np.full_like(tableau[:-1, -1], np.inf), where=tableau[:-1, pivot_col] > 0
        )
        pivot_row = np.argmin(ratios)

        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] /= pivot_element
        for i in range(len(tableau)):
            if i != pivot_row:
                tableau[i, :] -= tableau[i, pivot_col] * tableau[pivot_row, :]


    solution = np.zeros(num_vars)
    for i in range(num_constraints):
        basic_var_col = np.where(tableau[i, :num_vars] == 1)[0]
        print(basic_var_col)
        if len(basic_var_col) == 1:
            solution[basic_var_col[0]] = tableau[i, -1]

    print(tableau)
    return solution, tableau[-1, -1]


c = [-2, 3, -4]
A = [
    [1, 3, 5],
    [1, 1, 1],
    [2, 1, 4]
]
b = [15, 7, 12]

solution, max_value = simplex_method(c, A, b)
print(f"Optimal solution x: {solution}, Maximum value z: {max_value}")
