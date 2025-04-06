"""
GraphQL Schema Wrapper

This module binds together the Query and Mutation classes into a unified
GraphQL schema using Strawberry. It serves as the entry point for all
GraphQL operations exposed through the API.
"""

import strawberry
from app.graphql.resolvers.user_query import UserQuery
from app.graphql.mutations.user_mutation import UserMutation

# Create a Strawberry schema instance
# - Query: defines read-only operations (e.g., fetch users)
# - Mutation: defines write operations (e.g., register user)
schema = strawberry.Schema(
    query=UserQuery,
    mutation=UserMutation
)
