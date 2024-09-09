import random
import string

def _generate_id(name: str) -> str:
    random_chars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{name.lower().replace(' ', '_')}_{random_chars}"