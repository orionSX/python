import re


def is_valid_username(username):
    if isinstance(username, str) and 3 <= len(username) <= 20:
        if re.match(r"^[a-zA-Z0-9]+$", username):
            return True
    return False


def get_username(username):
    if not is_valid_username(username):
        raise ValueError(f"Некорректное имя пользователя: {username}")
    return username


try:
    user_input = "Alex#123"
    valid_name = get_username(user_input)
    print(f"Имя пользователя: {valid_name}")

except ValueError as e:
    print(e)
