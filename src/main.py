import asyncio
import logging

from fastapi import FastAPI

from src.health.schemas import HealthModel
from src.health.utils import is_mongodb_connected
from src.pokemon.routers import router as pokemon_router
from src.utils.load_data import fetch_and_save_pokemon_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., INFO, DEBUG, ERROR)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)

# Create app
app = FastAPI()
# Add router
app.include_router(pokemon_router)


# Fetch data from pokeapi and save to MongoDB
@app.on_event("startup")
async def save_pokemon_data():
    logger.info("Start downloading data...")
    tasks = [fetch_and_save_pokemon_data(n) for n in range(1, 152)]
    await asyncio.gather(*tasks)
    logger.info("Downloading was finished.")


# Health check (api + db)
@app.get("/", response_model=HealthModel, tags=["health"])
async def root():
    mongodb_task = asyncio.create_task(is_mongodb_connected())
    mongodb = await mongodb_task
    logger.info(f"Health endpoint: api - True, mongodb - {mongodb}")

    return {"api": True, "mongodb": mongodb}
