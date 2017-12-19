import secrets

def generate_token(user_dict):
    print('Generating new session token.')
    return secrets.token_urlsafe(32)