from passlib.context import CryptContext


pwd = CryptContext(schemes=["bcrypt"],deprecated="auto")

class Hash():
    @staticmethod
    def encrypt(password:str):
        return pwd.hash(password)

    @staticmethod
    def verify_password(password:str,hash:str):
        return pwd.verify(password,hash)
