import jwt

def generate_token(payload):
    token = jwt.encode(payload,'SECRET_KEY').decode('utf-8')
    return token