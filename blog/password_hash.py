from passlib.context import CryptContext


bcryptedpassword = CryptContext(schemes = ["bcrypt"] , deprecated = "auto")

class Hashed_password():
    def bcrypt(password:str):
        return bcryptedpassword.hash(password)
    def verify(hashed_password,plain_password):
        return bcryptedpassword.verify(plain_password,hashed_password)


