from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class InputBounds(BaseModel):
    """
    Bounding box for which we want to calculate the NDVI index
    """
    upper_left: tuple = Field(
        title="upper_left", description="upper left corner of the bounding box (lng, lat)")
    bottom_right: tuple = Field(
        title="bottom_right", description="bottom right corner of the bounding box (lng, lat)")

    class Config:
        schema_extra = {
            "example": {
                "upper_left": (-58.548340, -34.604787),
                "bottom_right": (-58.519157, -34.620478)
            }
        }
