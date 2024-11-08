import random
import string


def generate_random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{generate_random_string()}@{generate_random_string()}.com"
