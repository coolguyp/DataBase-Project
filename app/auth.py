import jwt
from datetime import datetime, timedelta

SECRET_KEY = "supersecretkey"

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

