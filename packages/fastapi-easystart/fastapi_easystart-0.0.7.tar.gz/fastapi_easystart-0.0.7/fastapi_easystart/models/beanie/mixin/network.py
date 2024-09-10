from typing import Optional

from pydantic import ConfigDict, Field, BaseModel


class NetworkDetailsModelMixin(BaseModel):
    ip_address: Optional[str] = Field(None, description="IP address of the user")
    network_provider: Optional[str] = Field(None, description="Network provider or ISP")
    network_type: Optional[str] = Field(None, description="Type of network (e.g., WiFi, Ethernet, Cellular)")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    class Config:
        json_schema_extra = {
            "example": {
                "ip_address": "192.168.1.1",
                "network_provider": "Comcast",
                "network_type": "WiFi"
            }
        }
