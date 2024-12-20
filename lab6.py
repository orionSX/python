import sqlite3
import json
from cgi import FieldStorage
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Создание базы данных и таблиц
def initialize_database():
    conn = sqlite3.connect("dance.db")
    cursor = conn.cursor()

    # Таблица танцоров
    cursor.execute('''CREATE TABLE IF NOT EXISTS dancers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        group_id INTEGER,
                        FOREIGN KEY (group_id) REFERENCES dance_groups(id)
                      )''')

    # Таблица танцевальных коллективов
    cursor.execute('''CREATE TABLE IF NOT EXISTS dance_groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        city TEXT NOT NULL
                      )''')

    # Таблица стилей танцев
    cursor.execute('''CREATE TABLE IF NOT EXISTS dance_styles (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                      )''')

    # Таблица выступлений
    cursor.execute('''CREATE TABLE IF NOT EXISTS performances (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        group_id INTEGER,
                        style_id INTEGER,
                        date TEXT NOT NULL,
                        location TEXT NOT NULL,
                        FOREIGN KEY (group_id) REFERENCES dance_groups(id),
                        FOREIGN KEY (style_id) REFERENCES dance_styles(id)
                      )''')

    conn.commit()
    conn.close()

# Заполнение таблиц тестовыми данными
def populate_database():
    conn = sqlite3.connect("dance.db")
    cursor = conn.cursor()

    # Танцевальные коллективы
    cursor.executemany('''INSERT INTO dance_groups (name, city) VALUES (?, ?)''',
                       [("Star Dancers", "New York"),
                        ("Urban Moves", "Los Angeles"),
                        ("Ballet Grace", "San Francisco")])

    # Стили танцев
    cursor.executemany('''INSERT INTO dance_styles (name) VALUES (?)''',
                       [("Hip-Hop",), ("Ballet",), ("Salsa",)])

    # Танцоры
    cursor.executemany('''INSERT INTO dancers (name, age, group_id) VALUES (?, ?, ?)''',
                       [("Alice", 25, 1),
                        ("Bob", 30, 2),
                        ("Clara", 22, 3)])

    # Выступления
    cursor.executemany('''INSERT INTO performances (group_id, style_id, date, location) VALUES (?, ?, ?, ?)''',
                       [(1, 1, "2023-05-10", "Broadway"),
                        (2, 2, "2023-06-15", "LA Theater"),
                        (3, 3, "2023-07-20", "SF Opera House")])

    conn.commit()
    conn.close()

# CGI-сервер
class CGIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        conn = sqlite3.connect("dance.db")
        cursor = conn.cursor()

        # Получаем данные из таблицы танцоров
        cursor.execute('''SELECT dancers.id, dancers.name, dancers.age, dance_groups.name 
                          FROM dancers
                          LEFT JOIN dance_groups ON dancers.group_id = dance_groups.id''')
        dancers_data = cursor.fetchall()

        # Получаем данные из таблицы коллективов
        cursor.execute('''SELECT id, name, city FROM dance_groups''')
        groups_data = cursor.fetchall()

        # Получаем данные из таблицы стилей
        cursor.execute('''SELECT id, name FROM dance_styles''')
        styles_data = cursor.fetchall()

        # Получаем данные из таблицы выступлений
        cursor.execute('''SELECT performances.id, dance_groups.name, dance_styles.name, performances.date, performances.location 
                          FROM performances
                          LEFT JOIN dance_groups ON performances.group_id = dance_groups.id
                          LEFT JOIN dance_styles ON performances.style_id = dance_styles.id''')
        performances_data = cursor.fetchall()

        conn.close()

        # HTML-страница
        self.wfile.write(b"<html><head><title>Dance Database</title>")
        self.wfile.write(b"<style>")
        self.wfile.write(b"body {font-family: Arial, sans-serif; margin: 20px;} ")
        self.wfile.write(b"table {border-collapse: collapse; width: 100%; margin-bottom: 20px;} ")
        self.wfile.write(b"th, td {border: 1px solid #ddd; padding: 8px;} ")
        self.wfile.write(b"th {background-color: #f2f2f2;} ")
        self.wfile.write(b"form {margin-bottom: 20px;}")
        self.wfile.write(b"input, select {margin: 5px 0; padding: 5px; width: 100%; max-width: 400px;}")
        self.wfile.write(b"input[type=submit] {background-color: #4CAF50; color: white; border: none; padding: 10px 20px; cursor: pointer;}")
        self.wfile.write(b"input[type=submit]:hover {background-color: #45a049;}")
        self.wfile.write(b"</style>")
        self.wfile.write(b"</head><body>")
        self.wfile.write(b"<h1>Dance Database</h1>")

        # Формы добавления записей
        self.wfile.write(b"<h2>Add Dancer</h2>")
        self.wfile.write(b"<form method='POST'>")
        self.wfile.write(b"<input type='hidden' name='table' value='dancers'>")
        self.wfile.write(b"Name: <input type='text' name='name'><br>")
        self.wfile.write(b"Age: <input type='number' name='age'><br>")
        self.wfile.write(b"Group ID: <input type='number' name='group_id'><br>")
        self.wfile.write(b"<input type='submit' value='Add Dancer'>")
        self.wfile.write(b"</form>")

        self.wfile.write(b"<h2>Add Dance Group</h2>")
        self.wfile.write(b"<form method='POST'>")
        self.wfile.write(b"<input type='hidden' name='table' value='dance_groups'>")
        self.wfile.write(b"Name: <input type='text' name='name'><br>")
        self.wfile.write(b"City: <input type='text' name='city'><br>")
        self.wfile.write(b"<input type='submit' value='Add Dance Group'>")
        self.wfile.write(b"</form>")

        self.wfile.write(b"<h2>Add Dance Style</h2>")
        self.wfile.write(b"<form method='POST'>")
        self.wfile.write(b"<input type='hidden' name='table' value='dance_styles'>")
        self.wfile.write(b"Name: <input type='text' name='name'><br>")
        self.wfile.write(b"<input type='submit' value='Add Dance Style'>")
        self.wfile.write(b"</form>")

        self.wfile.write(b"<h2>Add Performance</h2>")
        self.wfile.write(b"<form method='POST'>")
        self.wfile.write(b"<input type='hidden' name='table' value='performances'>")
        self.wfile.write(b"Group ID: <input type='number' name='group_id'><br>")
        self.wfile.write(b"Style ID: <input type='number' name='style_id'><br>")
        self.wfile.write(b"Date: <input type='date' name='date'><br>")
        self.wfile.write(b"Location: <input type='text' name='location'><br>")
        self.wfile.write(b"<input type='submit' value='Add Performance'>")
        self.wfile.write(b"</form>")

        # Отображение данных
        self.wfile.write(b"<h2>Dancers</h2>")
        self.wfile.write(b"<table><tr><th>ID</th><th>Name</th><th>Age</th><th>Group</th></tr>")
        for row in dancers_data:
            self.wfile.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>".encode())
        self.wfile.write(b"</table>")

        self.wfile.write(b"<h2>Dance Groups</h2>")
        self.wfile.write(b"<table><tr><th>ID</th><th>Name</th><th>City</th></tr>")
        for row in groups_data:
            self.wfile.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>".encode())
        self.wfile.write(b"</table>")

        self.wfile.write(b"<h2>Dance Styles</h2>")
        self.wfile.write(b"<table><tr><th>ID</th><th>Name</th></tr>")
        for row in styles_data:
            self.wfile.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>".encode())
        self.wfile.write(b"</table>")

        self.wfile.write(b"<h2>Performances</h2>")
        self.wfile.write(b"<table><tr><th>ID</th><th>Group</th><th>Style</th><th>Date</th><th>Location</th></tr>")
        for row in performances_data:
            self.wfile.write(f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>".encode())
        self.wfile.write(b"</table>")

        self.wfile.write(b"</body></html>")

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        fields = parse_qs(post_data)

        table = fields.get("table", [None])[0]

        conn = sqlite3.connect("dance.db")
        cursor = conn.cursor()

        if table == "dancers":
            name = fields.get("name", [None])[0]
            age = fields.get("age", [None])[0]
            group_id = fields.get("group_id", [None])[0]

            if age is not None:
                age = int(age)
            if group_id is not None:
                group_id = int(group_id)

            cursor.execute(
                '''INSERT INTO dancers (name, age, group_id) VALUES (?, ?, ?)''',
                (name, age, group_id))

        elif table == "dance_groups":
            name = fields.get("name", [None])[0]
            city = fields.get("city", [None])[0]

            cursor.execute(
                '''INSERT INTO dance_groups (name, city) VALUES (?, ?)''',
                (name, city))

        elif table == "dance_styles":
            name = fields.get("name", [None])[0]

            cursor.execute(
                '''INSERT INTO dance_styles (name) VALUES (?)''',
                (name,))

        elif table == "performances":
            group_id = fields.get("group_id", [None])[0]
            style_id = fields.get("style_id", [None])[0]
            date = fields.get("date", [None])[0]
            location = fields.get("location", [None])[0]

            if group_id is not None:
                group_id = int(group_id)
            if style_id is not None:
                style_id = int(style_id)

            cursor.execute(
                '''INSERT INTO performances (group_id, style_id, date, location) VALUES (?, ?, ?, ?)''',
                (group_id, style_id, date, location))

        conn.commit()
        conn.close()

        self.wfile.write(b"<html><body><h1>Data Added Successfully</h1>")
        self.wfile.write(b"<a href='/'>Back</a></body></html>")

if __name__ == "__main__":
    initialize_database()
    populate_database()

    server = HTTPServer(('localhost', 8000), CGIHandler)
    print("Server started at http://localhost:8000")
    server.serve_forever()
