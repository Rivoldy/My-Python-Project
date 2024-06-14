import random
import string
from hashlib import sha256
from datetime import datetime

def secure_random_choice(seq):
    """ Generate a secure random choice from a given sequence using hash function for better randomness. """
    hash_seed = sha256(f"{random.getrandbits(256)}".encode()).digest()
    seed = int.from_bytes(hash_seed, 'big')
    random.seed(seed)
    return random.choice(seq)

def generate_password(length=12):
    """ Generate a highly secure password. """
    if length < 12:  # Ensure minimum length for security
        raise ValueError("Password length must be at least 12 characters for security reasons.")
    
    # Character sets to choose from
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    unicode_chars = ''.join(chr(i) for i in range(1000, 1100))  # Adding some unicode characters for complexity

    # Ensure the password includes at least one character from each category
    password = [
        secure_random_choice(lower),
        secure_random_choice(upper),
        secure_random_choice(digits),
        secure_random_choice(symbols),
        secure_random_choice(unicode_chars)
    ]
    
    # Fill the rest of the password length
    while len(password) < length:
        password.append(secure_random_choice(lower + upper + digits + symbols + unicode_chars))
    
    random.shuffle(password)  # Shuffle to ensure randomness
    return ''.join(password)

# Example usage
print(generate_password(16))  # Generate a 16-character password
