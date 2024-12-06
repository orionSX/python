import math


class ShapeError(Exception):

    pass


class Shape:
  
    def __init__(self, identifier, *coordinates):
        self.identifier = identifier
        self.coordinates = list(coordinates)  

    def move(self, dx, dy):
        
        self.coordinates = [(x + dx, y + dy) for x, y in self.coordinates]

    def area(self):
        
        raise NotImplementedError("Этот метод должен быть реализован в подклассе.")


class Triangle(Shape):
    def area(self):
        
        if len(self.coordinates) != 3:
            raise ShapeError("Треугольник должен иметь 3 вершины.")
        x1, y1 = self.coordinates[0]
        x2, y2 = self.coordinates[1]
        x3, y3 = self.coordinates[2]
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)


class Tetragon(Shape):
    def area(self):
        
        if len(self.coordinates) != 4:
            raise ShapeError("Четырехугольник должен иметь 4 вершины.")
        x1, y1 = self.coordinates[0]
        x2, y2 = self.coordinates[1]
        x3, y3 = self.coordinates[2]
        x4, y4 = self.coordinates[3]
        return abs((x1 * y2 + x2 * y3 + x3 * y4 + x4 * y1 -
                    (y1 * x2 + y2 * x3 + y3 * x4 + y4 * x1)) / 2)


def is_include(t1, t2):
  
    def is_point_in_triangle(p, a, b, c):
        
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(p, a, b)
        d2 = sign(p, b, c)
        d3 = sign(p, c, a)
        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
        return not (has_neg and has_pos)

    if not isinstance(t1, Triangle):
        raise ShapeError("Первый объект должен быть треугольником.")
    if not isinstance(t2, Tetragon):
        raise ShapeError("Второй объект должен быть четырехугольником.")

    a, b, c = t1.coordinates
    for point in t2.coordinates:
        if not is_point_in_triangle(point, a, b, c):
            return False
    return True



if __name__ == "__main__":
    try:
        triangle = Triangle("Triangle1", (0, 0), (5, 0), (2, 5))
        tetragon = Tetragon("Tetragon1", (1, 1), (4, 1), (4, 4), (1, 4))

        print(f"Координаты треугольника: {triangle.coordinates}")

        triangle.move(1, 1)
        print(f"Новые координаты треугольника: {triangle.coordinates}")

     
        if is_include(triangle, tetragon):
            print("Четырехугольник полностью включен в треугольник.")
        else:
            print("Четырехугольник не включен в треугольник.")

    except ShapeError as e:
        print(f"Ошибка: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
