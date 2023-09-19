import logging
from typing import Union

import aiohttp

from src.database.database import db

KEYS_TO_KEEP = ["name", "abilities", "stats"]
STATS_KEY_TO_KEEP = ["hp", "attack", "defense", "speed"]
ABILITIES_KEY = "abilities"
STATS_KEY = "stats"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create a logger instance
logger = logging.getLogger(__name__)


async def fetch_and_save_pokemon_data(n: int) -> None:
    """
    Get pokemon's data from https://pokeapi.co/api/v2 and save in MongoDB
    :param n: int, pokemon's id
    :return: None
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://pokeapi.co/api/v2/pokemon/{n}"

        async with session.get(url) as response:
            raw_data = await response.json()
            data = filter_data(raw_data)

            await db["pokemon"].insert_one(data)
            logger.info(
                f"Data from https://pokeapi.co/api/v2/pokemon/{n} was fetched and saved in DB."
            )


def filter_data(raw_data: dict) -> dict:
    """Filter pokemon's data, stay only keys:
    - name
    - abilities
    - stats
    """
    data = {}
    for key, value in raw_data.items():
        if key in KEYS_TO_KEEP:
            if key == "name":
                data[key] = value
            else:
                data[key] = filter_nested_data(key, value)

    return data


def filter_nested_data(key: str, raw_data: dict) -> Union[dict, list]:
    """
    Filter nested lists depends on key
    :param key: ABILITIES_KEY or STATS_KEY
    :param raw_data: nested list for keys 'abilities' or 'stats'
    :return: filtered data
    """
    data = None

    # Fetch data for abilities
    if key == ABILITIES_KEY:
        data = list()

        for ability in raw_data:
            ability_data = {}

            ability_summary = ability.get("ability")
            if ability:
                ability_data["name"] = ability_summary.get("name")
                ability_data["url"] = ability_summary.get("url")

            data.append(ability_data)

    # Fetch data for stats
    elif key == STATS_KEY:
        stats_data = {}

        for stat in raw_data:
            stat_summary = stat.get("stat")
            if stat_summary and stat_summary.get("name") in STATS_KEY_TO_KEEP:
                stat_name = stat_summary.get("name")
                stats_data[stat_name] = stat.get("base_stat")

        data = stats_data

    return data
