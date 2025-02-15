import secrets
import hashlib
import string

def generate_secure_password(salt: str, length: int = 16) -> str:
    # Generate a random string of specified length
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    
    # Combine with salt and hash using SHA-256
    combined = salt + random_string
    hashed = hashlib.sha256(combined.encode()).hexdigest()
    
    # Return first 16 characters (64 bits) of the hash
    return hashed


def main():
    salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
    password = generate_secure_password(salt)
    print(password)


if __name__ == "__main__":
    main()
