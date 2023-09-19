from pydantic import BaseModel


class HealthModel(BaseModel):
    """Schema for health endpoint."""

    api: bool
    mongodb: bool
