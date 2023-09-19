from bson import ObjectId
from pydantic import BaseModel, Field

from src.database.database import PyObjectId


class AbilityModel(BaseModel):
    """Nested class for pokemon's abilities."""

    name: str
    url: str


class StatsModel(BaseModel):
    """Nested class for pokemon's stats."""

    hp: int = Field(ge=0)
    attack: int = Field(ge=0)
    defense: int = Field(ge=0)
    speed: int = Field(ge=0)


class PokemonModel(BaseModel):
    """Main model contains all data about pokemon."""

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    abilities: list[AbilityModel]
    stats: StatsModel

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "bulbasaur",
                "abilities": [
                    {
                        "ability_name": "overgrow",
                        "ability_url": "https://pokeapi.co/api/v2/ability/65/",
                    },
                    {
                        "ability_name": "chlorophyll",
                        "ability_url": "https://pokeapi.co/api/v2/ability/34/",
                    },
                ],
                "stats": {"hp": 45, "attack": 49, "defence": 49, "speed": 45},
            }
        }
