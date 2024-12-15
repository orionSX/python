import numpy as np
import matplotlib.pyplot as plt

def find_intersections(expr1, expr2, expr3, expr4):
    x1_values = np.linspace(0, 20, 400)
    intersections = []

    for x1 in x1_values:
        x2_values = np.linspace(0, 20, 400)
        for x2 in x2_values:
        
            if (
                abs(eval(expr1)) and
                abs(eval(expr2))  and
                abs(eval(expr3))  and
                abs(eval(expr4)) 
            ):
                intersections.append((x1, x2))

    return intersections


def linear_programming_graphic():
    
    x1 = np.linspace(0, 20, 400)  # x1 range

    
    y1 = (12 - 3 * x1) / -4  # 3x1 - 4x2 <= 12
    y2 = x1 + 2  # x1 - x2 >= -2
    y3 = (6 - 3 * x1)  # 3x1 + x2 >= 6
    y4 = (36 - 3 * x1) / 4  # 3x1 + 4x2 <= 36

    e1="3*x1 - 4*x2 <= 12"
    e2="x1 - x2 >= -2"
    e3="3*x1 + x2 >= 6"
    e4="3*x1 + 4*x2 <= 36"
  
    x1_grid, x2_grid = np.meshgrid(np.linspace(0, 20, 400), np.linspace(0, 20, 400))
    mask = (
            (3 * x1_grid - 4 * x2_grid <= 12) &
            (x1_grid - x2_grid >= -2) &
            (3 * x1_grid + x2_grid >= 6) &
            (3 * x1_grid + 4 * x2_grid <= 36) &
            (x1_grid >= 0) & (x2_grid >= 0)
    )

 
    plt.figure(figsize=(10, 8))
    plt.plot(x1, y1, label='3x1 - 4x2 <= 12')
    plt.plot(x1, y2, label='x1 - x2 >= -2')
    plt.plot(x1, y3, label='3x1 + x2 >= 6')
    plt.plot(x1, y4, label='3x1 + 4x2 <= 36')

   
    plt.contourf(x1_grid, x2_grid, mask, levels=[0.5, 1], colors=['lime'], alpha=0.3)

    # Plot objective function z = x1 + x2
    for z in range(5, 30, 5):
        plt.plot(x1, z - x1, '--', label=f'z = {z}')


    vertices =find_intersections(e1,e2,e3,e4)

    feasible_vertices = [
        v for v in vertices if
        (3 * v[0] - 4 * v[1] <= 12) and
        (v[0] - v[1] >= -2) and
        (3 * v[0] + v[1] >= 6) and
        (3 * v[0] + 4 * v[1] <= 36) and
        (v[0] >= 0) and (v[1] >= 0)
    ]

   
    z_values = [v[0] + v[1] for v in feasible_vertices]
    z_max = max(z_values)
    z_min = min(z_values)
    max_vertex = feasible_vertices[z_values.index(z_max)]
    min_vertex = feasible_vertices[z_values.index(z_min)]


    

    normal_vector = (1, 1)
    for z in range(5, 30, 5):
        plt.quiver(0, 0, normal_vector[0], normal_vector[1], angles='xy', scale_units='xy', scale=0.5, color='blue', alpha=0.5)
        plt.text(normal_vector[0] * 1.5, normal_vector[1] * 1.5, 'grad', color='blue')

    print(f'Maximum z: z = {z_max}, Vertex: {max_vertex}')
    print(f'Minimum z: z = {z_min}, Vertex: {min_vertex}')
    plt.scatter(*max_vertex, color='red')
    plt.text(max_vertex[0] + 0.2, max_vertex[1] + 0.2, f'({max_vertex[0]}, {max_vertex[1]})')
    plt.scatter(*min_vertex, color='red')
    plt.text(min_vertex[0] + 0.2, min_vertex[1] + 0.2, f'({min_vertex[0]}, {min_vertex[1]})')
    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title('Linear Programming Graphical Solution')

    plt.xlim(0, 10)
    plt.ylim(0, 10)

    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)

    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.legend()
    plt.show()

 
    


linear_programming_graphic()
