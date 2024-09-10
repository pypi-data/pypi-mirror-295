from typing import Optional

from pydantic import ConfigDict, Field, BaseModel


class DeviceDetailsModelMixin(BaseModel):
    device_type: Optional[str] = Field(None, description="Type of device (e.g., smartphone, tablet, laptop)")
    os_name: Optional[str] = Field(None, description="Operating system of the device (e.g., Windows, iOS, Android)")
    os_version: Optional[str] = Field(None, description="Version of the operating system")
    browser_name: Optional[str] = Field(None, description="Browser used (e.g., Chrome, Firefox, Safari)")
    browser_version: Optional[str] = Field(None, description="Version of the browser")
    screen_resolution: Optional[str] = Field(None, description="Screen resolution (e.g., 1920x1080)")
    device_model: Optional[str] = Field(None, description="Model of the device (e.g., iPhone 12, Dell XPS 13)")
    hardware: Optional[str] = Field(None, description="Hardware details of the device (e.g., CPU, GPU)")
    is_mobile: Optional[bool] = Field(None, description="Indicates if the device is a mobile device")
    user_agent: Optional[str] = Field(None, description="User agent string of the device")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

    class Config:
        json_schema_extra = {
            "example": {
                "device_type": "laptop",
                "os_name": "Windows",
                "os_version": "10",
                "browser_name": "Chrome",
                "browser_version": "91.0",
                "screen_resolution": "1920x1080",
                "device_model": "Dell XPS 13",
                "hardware": "Intel Core i7, NVIDIA GTX 1650",
                "is_mobile": False,
                "user_agent": "Mozilla/5.0 (Linux; Android 11.0; Pixel 4 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
            }
        }
