from typing import Optional, Dict

from pydantic import ConfigDict, Field, BaseModel


class LocationDetailsModelMixin(BaseModel):
    """Nested model to store detailed location information."""
    address: Optional[str] = Field(None, description="Human-readable address of the user.")
    latitude: Optional[float] = Field(None, description="Latitude of the user's location.")
    longitude: Optional[float] = Field(None, description="Longitude of the user's location.")
    city: Optional[str] = Field(None, description="City of the user's location.")
    state: Optional[str] = Field(None, description="State of the user's location.")
    country: Optional[str] = Field(None, description="Country of the user's location.")
    postal_code: Optional[str] = Field(None, description="Postal code of the user's location.")
    additional_info: Optional[Dict[str, str]] = Field(None, description="Additional location-related information such as timezone and provider.")
    # geolocation_provider: Optional[str] = Field(None, description="Provider of the geolocation data.")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    class Config:
        json_schema_extra = {
            "example": {
                "address": "123 Main St",
                "latitude": 37.7749,
                "longitude": -122.4194,
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "postal_code": "94103",
                "additional_info": {
                    "timezone": "Pacific Time",
                    "geolocation_provider": "GOOGLE_MAPS",
                },
            }
        }
