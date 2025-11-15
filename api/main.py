import csv
from functools import lru_cache
import os
from typing import Annotated
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
import csv
import os
from broker import publish_to_rabbitmq
from config import Settings
import pandas as pd

description = """
Microservice boilerplate 🚀

## Usage
- Pass foo data to any of API's endpoints (You can use foo data from down below)
- Look up to your terminal

{ 
"id": 50, 
"user_id": 12, 
"title": "Hello world", 
"description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.", 
"category_id": 4, 
"price": "5000" 
}



"""

settings = Settings()
security = HTTPBearer()
app = FastAPI(description=description)
BOOKS_CACHE = []


@lru_cache
def get_settings():
    return Settings()


@app.post("/api/user/subscribe")
def subscribe_user(data: dict, settings: Annotated[Settings, Depends(get_settings)]):
    publish_to_rabbitmq(
        queue_name=settings.queue_name_to_first_service,
        exchanger=settings.exchanger,
        routing_key=settings.routing_key_to_first_service,
        data=data
    )
    return {"detail": "User subscribed."}

@app.on_event("startup")
def load_csv_once():
    global BOOKS_CACHE
    df = pd.read_csv("/api/resource/books.csv", dtype=str).fillna("")
    BOOKS_CACHE = df.to_dict(orient="records")
    print(f"Loaded {len(BOOKS_CACHE)} books into memory")

@app.post("/api/order/checkout")
async def user_cart(data: dict, settings: Annotated[Settings, Depends(get_settings)]):
    await publish_to_rabbitmq(
        queue_name=settings.queue_name_to_cart_order,
        exchanger=settings.exchanger,
        routing_key=settings.routing_key_to_cart_order,
        data=data
    )
    return {"detail": "Order created."}

@app.get("/api/book/details")
def book_details(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Validate JWT first
    user = validate_jwt(credentials)
    return BOOKS_CACHE[:2000]

    csv_file_path = "/api/resource/books.csv"  # adjust to your real path

    if not os.path.exists(csv_file_path):
        raise HTTPException(status_code=404, detail=f"book.csv not found {csv_file_path}")

    books = []

    df = pd.read_csv("resource/books.csv", dtype=str).fillna("")
    return df.to_dict(orient="records")




JWT_SECRET = "S9!dK2#pL8@qR4%vT1*eW6&yZ3$hN7^bF5!sG0@tM4#pC8%rQ2*eH6&uL9$zB1^"
JWT_ALGO = "HS256"
def validate_jwt(credentials: HTTPAuthorizationCredentials):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="debug", reload=True)
