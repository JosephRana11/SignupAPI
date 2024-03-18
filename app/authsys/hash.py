from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default= "pbkdf2_sha256",
    )

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(password , user_password):
    hashed = encrypt_password(password)
    return password == user_password