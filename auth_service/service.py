# auth_service/auth_service.py
# auth_service.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from google_oauth import get_google_user_info, get_google_login_url
from jwt_utils import create_jwt_token, decode_jwt_token
from publish import publish_to_rabbitmq


app = FastAPI(title="Auth Service")

# Simple role assignment (can be replaced with DB)
USER_ROLES = {
    "m25ai1018@iitj.ac.in": "admin",
}

def get_role(email: str):
    return USER_ROLES.get(email, "customer")


@app.get("/auth/login")
async def login():
    """
    Redirect user to Google OAuth login page
    """
    
    url = get_google_login_url()
    return RedirectResponse(url)


@app.get("/auth/callback")
async def auth_callback(request: Request):

    FRONTEND_URL = "http://localhost:8080/"  # Angular route

    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code in callback")

    # <-- remove await
    user_info = get_google_user_info(code)
    email = user_info.get("email")
    name = user_info.get("name")
    google_id = user_info.get("sub")
    picture = user_info.get("picture") 

    # Assign role
    role = get_role(email)

    # Create JWT
    token = create_jwt_token(user_id=google_id, email=email, role=role)

    # Publish event to RabbitMQ
    event_data = {
        "user_id": google_id,
        "email": email,
        "role": role,
        "event": "user_authenticated",
        "picture":picture,
        "name":name

    }
    publish_to_rabbitmq(
        queue_name="user_events",
        exchanger="user_exchange",
        routing_key="user.authenticated",
        data=event_data
    )

    redirect_url = f"{FRONTEND_URL}?token={token}&name={name}&role={role}&picture={picture}"
    return RedirectResponse(url=redirect_url)



@app.get("/auth/me")
async def me(token: str = Depends(lambda request: request.headers.get("Authorization"))):
    """
    Returns info about the logged-in user based on JWT
    """
    from jwt_utils import decode_jwt_token
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        token_data = decode_jwt_token(token.replace("Bearer ", ""))
        return token_data
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
