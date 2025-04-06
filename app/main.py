"""
Main entry point for the Chrome Tour FastAPI application with GraphQL support.

This module initializes the FastAPI app, sets up the GraphQL router using Strawberry,
creates the database tables on startup, and registers event handlers such as
sending emails after user registration.
"""

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.models import Base
from app.database import engine
from app.graphql.schema import schema
from app.infrastructure.email.email_service import register_event_handlers

# Initialize the FastAPI app
app = FastAPI(
    title="Chrome Tour GraphQL API",
    description="A secure, extensible API built with FastAPI and Strawberry GraphQL",
    version="1.0.0",
)

# Mount the Strawberry GraphQL endpoint
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# Startup event: Create database tables and register event listeners
@app.on_event("startup")
async def on_startup():
    """
    Tasks to run when the application starts:
    - Create database tables if they don't exist.
    - Register user-related event handlers (e.g., email sending).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    register_event_handlers()  # 👈 Register email event listeners

# Optional HTTP root endpoint for testing
@app.get("/")
async def read_root():
    """
    Returns a welcome message with instructions.
    """
    return {"message": "Welcome to the Chrome Tour API! Visit /graphql to start querying."}
