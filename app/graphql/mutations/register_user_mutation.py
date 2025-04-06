"""
Strawberry GraphQL mutation class for user registration.
"""

import strawberry
from strawberry.types import Info
from app.schemas.user import UserRegisterInput, UserType
from app.core.services.user_service import UserService

@strawberry.type
class RegisterUserMutation:
    """
    GraphQL mutation class that handles user registration.
    """

    @strawberry.mutation
    async def register_user(
        self,
        input: UserRegisterInput,
        info: Info
    ) -> UserType:
        """
        Register a new user and return safe user details.

        Args:
            input (UserRegisterInput): The registration details.
            info (Info): Strawberry GraphQL context.

        Returns:
            UserType: Basic user profile excluding sensitive data.
        """
        return await UserService.register_user(input)
