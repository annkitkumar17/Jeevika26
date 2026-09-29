import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.notification_sync import TokenBlocklist, PasswordResetToken
from app.models.consent_privacy import AuditEvent
from app.schemas.token import UserRegister, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserRegister, is_admin_creator: bool = False) -> User:
        # Rule: Admin role cannot be self-registered publicly
        requested_role = user_in.role or "beneficiary"
        if requested_role == "admin" and not is_admin_creator:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Public registration with 'admin' role is prohibited. Admin accounts must be provisioned by an existing administrator."
            )

        existing_user = db.query(User).filter(User.email == user_in.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists."
            )
        
        user = User(
            email=user_in.email.lower(),
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            role=requested_role
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Audit event
        audit = AuditEvent(
            actor_id=user.id,
            actor_role=user.role,
            action="user_registered",
            resource_type="user",
            resource_id=user.id,
            details={"email": user.email, "role": user.role}
        )
        db.add(audit)
        db.commit()

        return user

    @staticmethod
    def authenticate_user(db: Session, login_in: UserLogin, ip_address: str = "127.0.0.1") -> dict:
        user = db.query(User).filter(User.email == login_in.email.lower()).first()
        if not user or not verify_password(login_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive."
            )
        
        access_token = create_access_token(subject=user.id, role=user.role)
        refresh_token = create_refresh_token(subject=user.id, role=user.role)
        
        # Audit event for login
        audit = AuditEvent(
            actor_id=user.id,
            actor_role=user.role,
            action="user_login",
            resource_type="user",
            resource_id=user.id,
            ip_address=ip_address,
            details={"email": user.email}
        )
        db.add(audit)
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "role": user.role,
            "user_id": user.id
        }

    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> dict:
        # Check if refresh token is in blocklist
        blocked = db.query(TokenBlocklist).filter(TokenBlocklist.jti == refresh_token).first()
        if blocked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has been revoked."
            )

        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token."
            )
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User no longer active or exists."
            )
        
        # Token rotation: revoke previous refresh token and issue a fresh pair
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        revoked_entry = TokenBlocklist(jti=refresh_token, expires_at=expires_at)
        db.add(revoked_entry)
        db.commit()

        new_access_token = create_access_token(subject=user.id, role=user.role)
        new_refresh_token = create_refresh_token(subject=user.id, role=user.role)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "role": user.role,
            "user_id": user.id
        }

    @staticmethod
    def revoke_token(db: Session, token: str):
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        block = TokenBlocklist(jti=token, expires_at=expires_at)
        db.add(block)
        db.commit()

    @staticmethod
    def request_password_reset(db: Session, email: str) -> str:
        user = db.query(User).filter(User.email == email.lower()).first()
        if not user:
            # Return dummy success to prevent email enumeration
            return "If the account exists, a reset link was generated."
        
        reset_token = str(uuid.uuid4())
        reset_entry = PasswordResetToken(
            user_id=user.id,
            token=reset_token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=2)
        )
        db.add(reset_entry)
        db.commit()
        return reset_token

    @staticmethod
    def confirm_password_reset(db: Session, token: str, new_password: str):
        reset_entry = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == token,
            PasswordResetToken.is_used == False,
            PasswordResetToken.expires_at > datetime.now(timezone.utc)
        ).first()
        if not reset_entry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired password reset token."
            )
        
        user = db.query(User).filter(User.id == reset_entry.user_id).first()
        if user:
            user.hashed_password = get_password_hash(new_password)
            reset_entry.is_used = True
            db.commit()
