"""
Service layer for core user operations like registration and verification.
"""

from app.models import User
from app.schemas.user import UserRegisterInput, UserType, UserVerifyInput
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import secrets
import re
from sqlalchemy.exc import IntegrityError
from graphql import GraphQLError
from app.events.user_events import event_bus

class UserService:
    """
    Contains business logic for user-related workflows.
    """

    @staticmethod
    async def register_user(input: UserRegisterInput) -> UserType:
        """
        Register a new user with full validation, hashing, and setup.

        This method performs:
        - Email format validation
        - Uniqueness checks for username, email, and phone number
        - Password hashing
        - Verification code generation
        - Registration metadata tracking

        Args:
            input (UserRegisterInput): The registration input object.

        Raises:
            GraphQLError: When one or more fields fail validation.

        Returns:
            UserType: A sanitized public-facing user type for API response.
        """
        db: AsyncSession = await get_db().__anext__()

        errors = {}

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", input.email):
            errors["email"] = "Invalid email format."

        # Check username uniqueness
        result = await db.execute(select(User).where(User.username == input.username))
        if result.scalars().first():
            errors["username"] = "Username is already taken."

        # Check email uniqueness
        result = await db.execute(select(User).where(User.email == input.email))
        if result.scalars().first():
            errors["email"] = "Email is already registered."

        # Check phone number uniqueness (if provided)
        if input.phone_number:
            result = await db.execute(select(User).where(User.phone_number == input.phone_number))
            if result.scalars().first():
                errors["phone_number"] = "Phone number is already in use."

        if errors:
            # Aggregate all field errors and raise as GraphQLError
            formatted = "\n".join(f"{field}: {msg}" for field, msg in errors.items())
            raise GraphQLError(f"Registration failed:\n{formatted}")

        # Hash the password using bcrypt
        hashed_password = bcrypt.hash(input.password)

        # Generate verification code
        verification_code = secrets.token_hex(3)
        expires_at = datetime.utcnow() + timedelta(minutes=10)

        # Create new user
        new_user = User(
            username=input.username,
            email=input.email,
            phone_number=input.phone_number,
            password_hash=hashed_password,
            is_active=False,
            email_verified=False,
            verification_code=verification_code,
            verification_code_expires_at=expires_at,
            registration_ip=input.registration_ip,
            registration_user_agent=input.user_agent,
            registered_via=input.registered_via,
            registration_referrer=input.registration_referrer,
        )

        db.add(new_user)
        try:
            await db.commit()
        except IntegrityError:
            await db.rollback()
            raise GraphQLError("Unexpected database error while saving user.")

        await db.refresh(new_user)

        await event_bus.emit_async("user_registered", new_user)

        return UserType(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            is_active=new_user.is_active,
            email_verified=new_user.email_verified
        )

    @staticmethod
    async def verify_user_code(input: UserVerifyInput, db: AsyncSession) -> UserType:
        """
        Verify a user's email or phone using a verification code.

        Args:
            input (UserVerifyInput): Contains email_or_phone and verification_code.
            db (AsyncSession): Database session.

        Raises:
            ValueError: If no user is found, or code is invalid/expired.

        Returns:
            UserType: Verified user info.
        """
        query = select(User).where(
            (User.email == input.email_or_phone) | (User.phone_number == input.email_or_phone)
        )
        result = await db.execute(query)
        user = result.scalars().first()

        if not user:
            raise ValueError("User not found.")

        if user.verification_code != input.verification_code:
            raise ValueError("Invalid verification code.")

        if not user.verification_code_expires_at or user.verification_code_expires_at < datetime.utcnow():
            raise ValueError("Verification code has expired.")

        user.email_verified = True
        user.email_verified_at = datetime.utcnow()
        user.is_active = True  # optional depending on your flow

        await db.commit()
        await db.refresh(user)

        return UserType(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            email_verified=user.email_verified
        )

