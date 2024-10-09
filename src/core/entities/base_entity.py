# src/core/entities/base_entity.py

from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional


class BaseEntity(BaseModel):
    """Base entity with common fields for all entities."""
    created: Optional[datetime] = Field(default_factory=datetime.utcnow)
    modified: Optional[datetime] = Field(default_factory=datetime.utcnow)
    deleted: Optional[datetime] = None

    @model_validator(mode='before')
    @classmethod
    def set_modified(cls, values):
        """Automatically update the 'modified' field."""
        values["modified"] = datetime.utcnow()
        return values

    class Config:
        # Configuration to allow aliasing fields and arbitrary types (if needed)
        populate_by_name = True
        arbitrary_types_allowed = True

