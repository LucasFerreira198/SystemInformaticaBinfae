import bcrypt

def gerateHashPassword(password_clear: str) -> str:
    """transforma a senha em texto puro em um hash seguro"""
    pwd_bytes = password_clear.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

def verifyPassword(password_clear: str, password_hash: str) -> str:
    """Verifica se a senha enviada corresponde ao hash salvo no banco"""
    pwd_bytes = password_clear.encode('utf-8')[:72]
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)