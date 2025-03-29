from fastapi import Request, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from .database import SUPABASE_JWT_SECRET

security = HTTPBearer()

async def auth_middleware(request: Request, call_next):
    """Middleware to authenticate requests using JWT."""
    token = request.cookies.get('access_token')
    if token and token.startswith("Bearer "):
        token = token.split(" ")[1]
        request.headers.__dict__["list"].append(
            (b"Authorization", f"Bearer {token}".encode()))
        
    response = await call_next(request)
    return response

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        if token and token.startswith("Bearer "):
            token = token.split(" ")[1] # Ensure correct import for PyJWT
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"],options={"verify_signature": False})
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth creds")
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")