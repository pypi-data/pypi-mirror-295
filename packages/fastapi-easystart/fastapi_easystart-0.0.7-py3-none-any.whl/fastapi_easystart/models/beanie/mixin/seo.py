from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, validator

from src.app.utils import CustomRobotTagsEnum


# Define your choice enums
class CustomRobotTags(str, Enum):
    DEFAULT = "default"
    NOINDEX = "noindex"


class SeoFieldMixinModel(BaseModel):
    title: str = Field(..., description="A human-readable title given to the resource and also for the SEO meta tag.")
    keyword: Optional[str] = Field(None, description="Keywords for SEO.")
    description: Optional[str] = Field(None, description="A short description of the resource and also for SEO.")
    custom_robot_tags: List[CustomRobotTagsEnum] = Field(default=[], description="Custom robot tags for SEO.")

    @validator('custom_robot_tags', pre=True)
    def validate_custom_robot_tags(cls, v):
        allowed_tags = {tag.value for tag in CustomRobotTagsEnum}
        if not all(tag in allowed_tags for tag in v):
            raise ValueError(f"Invalid tags: {set(v) - allowed_tags}. Must be one of {allowed_tags}")
        return v
