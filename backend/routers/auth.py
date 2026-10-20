
import json
import os
from datetime import datetime, timedelta
from urllib.parse import parse_qs

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from passlib.context import CryptContext
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserRegister, UserLogin, Token


load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def create_token(user_id: int, email: str) -> str:
    secret_key = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")
    expiry_minutes = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120")
    )

    if not secret_key:
        raise RuntimeError("SECRET_KEY is not configured.")

    expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)

    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
    }

    return jwt.encode(payload, secret_key, algorithm=algorithm)


def verify_password(password: str, hashed_password: str) -> bool:
    # Preserve compatibility with the existing bcrypt password hashes.
    # bcrypt uses a maximum input length of 72 bytes.
    password_bytes = password.encode("utf-8")[:72]

    try:
        return pwd_context.verify(
            password_bytes.decode("latin-1"),
            hashed_password,
        )
    except (ValueError, TypeError):
        return False


def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")[:72]

    return pwd_context.hash(
        password_bytes.decode("latin-1")
    )


@router.post("/register", response_model=Token)
def register(
    user: UserRegister,
    db: Session = Depends(get_db),
):
    email = user.email.strip().lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    new_user = User(
        name=user.name,
        email=email,
        mobile_number=user.mobile_number,
        hashed_password=hash_password(user.password),
        school=user.school,
        student_class=user.student_class,
        father_name=user.father_name,
        mother_name=user.mother_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "access_token": create_token(
            new_user.id,
            new_user.email,
        ),
        "token_type": "bearer",
    }


async def get_login_credentials(request: Request) -> tuple[str, str]:
    """
    Accept either:
    1. JSON: {"email": "...", "password": "..."}
    2. OAuth2 form: username=...&password=...

    This allows the existing frontend and Swagger OAuth2 dialog
    to use the same login endpoint.
    """
    content_type = request.headers.get("content-type", "").lower()

    if "application/json" in content_type:
        try:
            data = await request.json()
        except (json.JSONDecodeError, ValueError):
            raise HTTPException(
                status_code=400,
                detail="Invalid JSON request body",
            )

        if not isinstance(data, dict):
            raise HTTPException(
                status_code=422,
                detail="Request body must be a JSON object",
            )

        email = data.get("email") or data.get("username")
        password = data.get("password")

    elif (
        "application/x-www-form-urlencoded" in content_type
        or not content_type
    ):
        body = (await request.body()).decode(
            "utf-8",
            errors="replace",
        )
        data = parse_qs(body, keep_blank_values=True)

        email = (
            data.get("username", [None])[0]
            or data.get("email", [None])[0]
        )
        password = data.get("password", [None])[0]

    else:
        raise HTTPException(
            status_code=415,
            detail="Use JSON or URL-encoded form data",
        )

    if not isinstance(email, str) or not email.strip():
        raise HTTPException(
            status_code=422,
            detail="Email or username is required",
        )

    if not isinstance(password, str) or not password:
        raise HTTPException(
            status_code=422,
            detail="Password is required",
        )

    return email.strip().lower(), password


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    db: Session = Depends(get_db),
):
    email, password = await get_login_credentials(request)

    db_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if (
        not db_user
        or not verify_password(
            password,
            db_user.hashed_password,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_token(
            db_user.id,
            db_user.email,
        ),
        "token_type": "bearer",
    }
