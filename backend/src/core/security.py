import bcrypt

def hash_password(password: str) -> str:
    """Gera o hash seguro a partir de uma senha em texto limpo."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara a senha em texto limpo enviada no login com o hash salvo no banco."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )