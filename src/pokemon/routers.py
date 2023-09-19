import logging
from typing import Annotated, Dict, Union

from fastapi import APIRouter, HTTPException, Path

from src.database.database import db
from src.pokemon.models import PokemonModel

router = APIRouter(
    prefix="/pokemon",
    tags=["Pokemons"],
)
collection = db["pokemon"]

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)


@router.get("/{name}", response_model=PokemonModel)
async def get_pokemon_info(name: str) -> Union[Dict, None]:
    logger.info(f"Request to /pokemon/{name}...")
    pokemon = await collection.find_one({"name": name})

    if not pokemon:
        logger.error(f"Error: Pokemon {name} is not in DB.")
        raise HTTPException(status_code=404, detail="Pokemon not found.")

    pokemon.pop("_id", None)
    logger.info(f"Successfully request for pokemon {name}: {pokemon}.")

    return pokemon


@router.get("/hp/{hp}")
async def get_pokemon_names_by_hp(hp: Annotated[int, Path(ge=0)]):
    logger.info(f"Request to /pokemon/hp/{hp}...")
    pokemon_list = await collection.find(
        {"stats.hp": {"$gt": hp}}, {"name": 1, "_id": 0}
    ).to_list(length=151)
    pokemon_names = [p["name"] for p in pokemon_list]
    logger.info(f"Pokemons with hp {hp}: {pokemon_names}.")

    return pokemon_names
