# auth_service/jwt_utils.py

import jwt
from datetime import datetime, timedelta

JWT_SECRET = "S9!dK2#pL8@qR4%vT1*eW6&yZ3$hN7^bF5!sG0@tM4#pC8%rQ2*eH6&uL9$zB1^"
JWT_ALGORITHM = "HS256"


def create_jwt_token(user_id:str,email: str, role: str):
    payload = {
        "user_id":user_id,
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token: str):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
