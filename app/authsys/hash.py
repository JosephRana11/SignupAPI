from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default= "pbkdf2_sha256",
    )

def encrypt_password(password):
    return pwd_context.encrypt(password)

def check_encrypted_password(plain_password , hashed_password):
    return pwd_context.verify(plain_password , hashed_password)