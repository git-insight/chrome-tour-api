"""Contains GraphQL resolvers related to the User entity."""

import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserType
from app.models import User
from app.database import async_session

@strawberry.type
class UserQuery:
    """GraphQL query operations for the User model."""

    @strawberry.field
    async def all_users(self) -> list[UserType]:
        """Returns all users in the system."""
        async with async_session() as session:
            result = await session.execute(
                User.__table__.select()
            )
            users = result.fetchall()
            return [
                UserType(
                    id=row.id,
                    username=row.username,
                    email=row.email,
                    is_active=row.is_active
                ) for row in users
            ]
