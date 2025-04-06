"""
Event dispatcher using pyee to decouple event emission from handling.
"""

from pyee.asyncio import AsyncIOEventEmitter

# Global event emitter for the app
event_bus = AsyncIOEventEmitter()
