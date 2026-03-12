from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password = "12345678"
hashed = pwd_context.hash(password)
print(f"Hashed: {hashed}")
print(f"Verified: {pwd_context.verify(password, hashed)}")
