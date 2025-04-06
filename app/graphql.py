import strawberry
from app.resolvers.user_resolver import Query

schema = strawberry.Schema(query=Query)
