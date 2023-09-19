from pymongo.errors import ConnectionFailure

from src.database.database import client


async def is_mongodb_connected() -> bool:
    """Get mongo db status."""
    try:
        await client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False
