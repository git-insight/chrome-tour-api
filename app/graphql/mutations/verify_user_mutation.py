"""
GraphQL mutation for verifying a user's registration using a code.
"""

import strawberry
from app.schemas.user import UserType, UserVerifyInput
from app.core.services.user_service import UserService
from app.database import get_db
from strawberry.types import Info

@strawberry.type
class VerifyUserMutation:
    """
    Contains the mutation to verify a user's identity using a verification code.
    """
    
    @strawberry.mutation
    async def verify_user(self, input: UserVerifyInput, info: Info) -> UserType:
        """
        Verify a user based on email/phone and code.
        """
        db = await get_db().__anext__()
        return await UserService.verify_user_code(input=input, db=db)
