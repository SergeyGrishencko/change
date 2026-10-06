from bcrypt import checkpw, gensalt, hashpw


def hashed_password(password: str) -> bytes:
    """Метод для хэширования пароля пользователя."""

    return hashpw(password.encode('utf-8'), gensalt())


def verify_password(password: str, hashed: bytes) -> bool:
    """Метод для верификации введенного пароля со значением в базе данных."""

    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    return checkpw(
        password=password.encode('utf-8'), 
        hashed_password=hashed_password,
    )