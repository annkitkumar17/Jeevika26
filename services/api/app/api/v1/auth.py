from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.token import UserRegister, UserLogin, Token, RefreshTokenRequest, UserResponse
from app.services.auth import AuthService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user (Beneficiary, Facilitator, or Admin).
    """
    user = AuthService.register_user(db, user_in)
    return user

@router.post("/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password to receive JWT access and refresh tokens.
    """
    token_data = AuthService.authenticate_user(db, login_in)
    return token_data

@router.post("/login/oauth", response_model=Token, include_in_schema=False)
def login_oauth(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    OAuth2 compatible token login for Swagger UI.
    """
    login_in = UserLogin(email=form_data.username, password=form_data.password)
    return AuthService.authenticate_user(db, login_in)

@router.post("/refresh", response_model=Token)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """
    Refresh an expired access token using a valid refresh token.
    """
    return AuthService.refresh_access_token(db, request.refresh_token)

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user session.
    """
    return {"message": "Successfully logged out", "user_id": current_user.id}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """
    Get profile information of currently authenticated user.
    """
    return current_user
