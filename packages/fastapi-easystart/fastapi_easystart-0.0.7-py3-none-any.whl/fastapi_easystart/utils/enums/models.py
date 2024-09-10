from fastapi_easystart.utils.enums.base import BaseCustomEnum


class GeolocationProviderEnum(BaseCustomEnum):
    # Common geolocation providers
    GEOIP = "GeoIP"
    GPS = "GPS"
    WIFI = "WiFi"
    CELLULAR = "Cellular"
    IP2LOCATION = "IP2Location"
    GOOGLE_MAPS = "Google Maps"
    OPENSTREETMAP = "OpenStreetMap"
    MAXMIND = "MaxMind"
    BING_MAPS = "Bing Maps"
    HERE = "HERE"
    IPINFO = "IPInfo"
    IPSTACK = "IPStack"
    OTHER = "Other"  # For any other provider not listed
