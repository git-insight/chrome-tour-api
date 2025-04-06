"""
GraphQL aggregator for all user-related mutations.
"""

import strawberry
from app.graphql.mutations.register_user_mutation import RegisterUserMutation
from app.graphql.mutations.verify_user_mutation import VerifyUserMutation

@strawberry.type
class UserMutation(RegisterUserMutation, VerifyUserMutation):
    """
    Combines all user-related mutations into one class.

    Extend this class to include additional user mutations such as verification,
    password reset, profile update, etc.
    """
    pass
