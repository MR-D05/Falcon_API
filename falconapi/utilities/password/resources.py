import bcrypt

def hash(password):
    password = password.encode('UTF-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt).decode('UTF-8')

def verify(password, hashed):
    password = password.encode('UTF-8')
    hashed = hashed.encode('UTF-8')
    return bcrypt.checkpw(password, hashed)