from typing import List, Literal, Optional

from mlx.misc.util import backfill
from mlx.models.base import BaseModel
from pydantic import PrivateAttr, field_validator, model_validator


class CmdParam(BaseModel):
    flag: str
    value: str


class CmdParams(BaseModel):
    params: List[CmdParam]


class Flags(BaseModel):
    audio_masking: Literal["mask", "natural"]
    graphics_noise: Literal["mask", "natural"]
    ports_masking: Literal["mask", "natural"]
    navigator_masking: Literal["natural", "custom", "mask"]
    localization_masking: Literal["natural", "custom", "mask"]
    timezone_masking: Literal["natural", "custom", "mask"]
    graphics_masking: Literal["natural", "custom", "mask"]
    fonts_masking: Literal["natural", "custom", "mask"]
    media_devices_masking: Literal["natural", "custom", "mask"]
    screen_masking: Literal["natural", "custom", "mask"]
    geolocation_masking: Literal["custom", "mask"]
    webrtc_masking: Literal["natural", "custom", "mask", "disabled"]
    proxy_masking: Literal["custom", "disabled"]
    geolocation_popup: Literal["prompt", "allow", "block"]

    @model_validator(mode="before")
    def validate_flags(cls, values):
        required_flags_fields = [
            "audio_masking",
            "fonts_masking",
            "geolocation_masking",
            "geolocation_popup",
            "graphics_masking",
            "graphics_noise",
            "localization_masking",
            "media_devices_masking",
            "navigator_masking",
            "ports_masking",
            "proxy_masking",
            "screen_masking",
            "timezone_masking",
            "webrtc_masking",
        ]
        for field in required_flags_fields:
            if field not in values:
                raise ValueError(f"Missing required field in flags: {field}")

        return values


class Navigator(BaseModel):
    hardware_concurrency: Literal[2, 4, 6, 8, 12, 16]
    platform: str
    user_agent: str
    os_cpu: Optional[str] = None

    @model_validator(mode="before")
    def validate_navigator(cls, values):
        required_fields = ["hardware_concurrency", "platform", "user_agent"]
        for field in required_fields:
            if field not in values:
                raise ValueError(f"Missing required field in navigator: {field}")

        if values["hardware_concurrency"] not in [2, 4, 6, 8, 12, 16]:
            raise ValueError(
                "Invalid value for hardware_concurrency in navigator fingerprint."
            )

        return values


class Localization(BaseModel):
    languages: str
    locale: str
    accept_languages: str

    @model_validator(mode="before")
    def validate_localization(cls, values):
        required_fields = ["languages", "locale", "accept_languages"]
        for field in required_fields:
            if field not in values:
                raise ValueError(f"Missing required field in localization: {field}")

        return values


class Timezone(BaseModel):
    zone: str

    @model_validator(mode="before")
    def validate_timezone(cls, values):
        if "zone" not in values:
            raise ValueError("Missing required field in timezone: zone")
        return values


class Graphic(BaseModel):
    renderer: str
    vendor: str
    vendor_id: Optional[str] = None
    renderer_id: Optional[str] = None

    @model_validator(mode="before")
    def validate_graphic(cls, values):
        required_fields = ["renderer", "vendor"]
        for field in required_fields:
            if field not in values:
                raise ValueError(f"Missing required field in graphic: {field}")
        return values


class Webrtc(BaseModel):
    public_ip: str

    @model_validator(mode="before")
    def validate_webrtc(cls, values):
        if "public_ip" not in values:
            raise ValueError("Missing required field in webrtc: public_ip")
        return values


class MediaDevices(BaseModel):
    audio_inputs: int
    audio_outputs: int
    video_inputs: int


class Screen(BaseModel):
    height: int
    pixel_ratio: float
    width: int

    @model_validator(mode="before")
    def validate_screen(cls, values):
        required_fields = ["height", "pixel_ratio", "width"]
        for field in required_fields:
            if field not in values:
                raise ValueError(f"Missing required field in screen: {field}")
        return values


class Geolocation(BaseModel):
    accuracy: float
    altitude: float
    latitude: float
    longitude: float


class Fingerprint(BaseModel):
    cmd_params: Optional[CmdParams] = None
    fonts: Optional[List[str]] = None
    geolocation: Optional[Geolocation] = None
    graphic: Optional[Graphic] = None
    localization: Optional[Localization] = None
    media_devices: Optional[MediaDevices] = None
    navigator: Optional[Navigator] = None
    ports: Optional[List[int]] = None
    screen: Optional[Screen] = None
    timezone: Optional[Timezone] = None
    webrtc: Optional[Webrtc] = None

    @model_validator(mode="before")
    def validate_fingerprint(cls, values):
        if navigator := values.get("navigator"):
            if (
                "hardware_concurrency" not in navigator
                or "platform" not in navigator
                or "user_agent" not in navigator
            ):
                raise ValueError("Missing required fields in navigator fingerprint.")
            if navigator["hardware_concurrency"] not in [2, 4, 6, 8, 12, 16]:
                raise ValueError(
                    "Invalid value for hardware_concurrency in navigator fingerprint."
                )

        if localization := values.get("localization"):
            if (
                "languages" not in localization
                or "locale" not in localization
                or "accept_languages" not in localization
            ):
                raise ValueError("Missing required fields in localization fingerprint.")

        if timezone := values.get("timezone"):
            if "zone" not in timezone:
                raise ValueError("Missing required field in timezone fingerprint.")

        if graphic := values.get("graphic"):
            if "renderer" not in graphic or "vendor" not in graphic:
                raise ValueError("Missing required fields in graphic fingerprint.")

        if webrtc := values.get("webrtc"):
            if "public_ip" not in webrtc:
                raise ValueError("Missing required field in webrtc fingerprint.")

        if screen := values.get("screen"):
            if (
                "height" not in screen
                or "pixel_ratio" not in screen
                or "width" not in screen
            ):
                raise ValueError("Missing required fields in screen fingerprint.")

        return values


class Proxy(BaseModel):
    host: str
    type: Literal["http", "socks"]
    port: int
    username: Optional[str] = None
    password: Optional[str] = None

    @property
    def url(self):
        if self.username and self.password:
            return (
                f"{self.type}://{self.username}:{self.password}@{self.host}:{self.port}"
            )
        return f"{self.type}://{self.host}:{self.port}"

    def active_check(self):
        import urllib3

        try:
            http = urllib3.ProxyManager(self.url, headers={"Connection": "keep-alive"})

            r = http.request("GET", "http://ifconfig.me")
            return_str = r.data
            return True if return_str else False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    @classmethod
    def from_env(cls, asdict=False):
        import os

        _cls = dict if asdict else cls
        return cls(
            host=os.getenv("PROXY_HOST", "default_host"),
            port=int(os.getenv("PROXY_PORT", 5959)),
            type=os.getenv("PROXY_TYPE", "http"),  # type: ignore
            username=os.getenv("PROXY_USERNAME", "default_username"),
            password=os.getenv("PROXY_PASSWORD", "default_password"),
        )

    @model_validator(mode="before")
    def validate_proxy(cls, values):
        required_fields = ["host", "type", "port"]
        for field in required_fields:
            if field not in values:
                raise ValueError(f"Missing required field in proxy: {field}")
        return values


class Storage(BaseModel):
    is_local: Optional[bool] = True
    save_service_worker: Optional[bool] = False


class Parameters(BaseModel):
    flags: Flags
    fingerprint: Fingerprint
    storage: Optional[Storage] = None
    notes: Optional[str] = None

    @model_validator(mode="before")
    def validate_model(cls, values):
        required_parameters_fields = ["flags", "fingerprint"]
        for field in required_parameters_fields:
            if field not in values:
                raise ValueError(f"Missing required field in parameters: {field}")

        required_flags_fields = [
            "audio_masking",
            "fonts_masking",
            "geolocation_masking",
            "geolocation_popup",
            "graphics_masking",
            "graphics_noise",
            "localization_masking",
            "media_devices_masking",
            "navigator_masking",
            "ports_masking",
            "proxy_masking",
            "screen_masking",
            "timezone_masking",
            "webrtc_masking",
        ]
        for field in required_flags_fields:
            if field not in values["flags"]:
                raise ValueError(f"Missing required field in parameters.flags: {field}")

        parameters_to_fingerprint = {
            "audio_masking": "audio",
            "fonts_masking": "fonts",
            "geolocation_masking": "geolocation",
            "graphics_masking": "graphic",
            "localization_masking": "localization",
            "media_devices_masking": "media_devices",
            "navigator_masking": "navigator",
            "ports_masking": "ports",
            "screen_masking": "screen",
            "timezone_masking": "timezone",
            "webrtc_masking": "webrtc",
        }

        for key, value in values["flags"].items():
            if value == "custom":
                lookup = parameters_to_fingerprint.get(key, None)
                if lookup is None:
                    continue
                if lookup not in values["fingerprint"]:
                    raise ValueError(
                        f"You must define {lookup} in parameters.fingerprint since {key} is set to 'custom'"
                    )

        return values


class Profile(BaseModel):
    browser_type: Literal["mimic", "stealthfox"]
    os_type: Literal["windows", "macos", "linux"]
    automation: Optional[Literal["selenium", "playwright", "puppeteer"]] = None
    core_version: Optional[int] = None
    is_headless: Optional[bool] = None
    proxy: Optional[Proxy] = None
    parameters: Parameters

    __default__ = {
        "browser_type": "mimic",
        "automation": "selenium",
        "os_type": "linux",
        "is_headless": False,
        "parameters": {
            "flags": {
                "audio_masking": "mask",
                "fonts_masking": "mask",
                "geolocation_masking": "mask",
                "geolocation_popup": "prompt",
                "graphics_masking": "mask",
                "graphics_noise": "mask",
                "proxy_masking": "custom",
                "localization_masking": "mask",
                "media_devices_masking": "mask",
                "navigator_masking": "mask",
                "ports_masking": "natural",
                "screen_masking": "mask",
                "timezone_masking": "mask",
                "webrtc_masking": "mask",
            },
            "storage": {"is_local": True, "save_service_worker": False},
            "fingerprint": {
                # "navigator": {
                #     "hardware_concurrency": 8,
                #     "platform": "Win32",
                #     "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                #     "os_cpu": "",
                # },
                # "localization": {
                #     "languages": "en-US",
                #     "locale": "en-US",
                #     "accept_languages": "en-US,en;q=0.5",
                # },
                # "timezone": {"zone": "Asia/Bangkok"},
                # "graphic": {
                #     "renderer": "ANGLE (NVIDIA, NVIDIA GeForce RTX 4070 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
                #     "vendor": "Google Inc. (NVIDIA)",
                # },
                # "webrtc": {"public_ip": "123.123.123.123"},
                # "media_devices": {
                #     "audio_inputs": 1,
                #     "audio_outputs": 1,
                #     "video_inputs": 2,
                # },
                # "screen": {"height": 1200, "pixel_ratio": 1, "width": 1920},
                # "geolocation": {
                #     "accuracy": 100,
                #     "altitude": 100,
                #     "latitude": 52.02,
                #     "longitude": -52.1,
                # },
                # "ports": [12345],
                # "fonts": ["81938139"],
                # "cmd_params": {
                #     "params": [{"flag": "show-fps-counter", "value": "true"}]
                # },
            },
        },
    }

    @classmethod
    def default(cls):
        return cls.model_validate(cls.__default__)

    @classmethod
    def with_defaults(cls, overrides):
        return cls.model_validate(
            backfill(
                cls.__default__,
                overrides,
            )
        )

    @model_validator(mode="before")
    def validate_body(cls, values):
        required_fields = ["browser_type", "os_type", "parameters"]
        for field in required_fields:
            if field not in values:
                raise ValueError(f"Missing required field: {field}")

        if values["browser_type"] not in ["mimic", "stealthfox"]:
            raise ValueError(
                "Invalid value for browser_type. Must be 'mimic' or 'stealthfox'."
            )

        if values["os_type"] not in ["linux", "macos", "windows"]:
            raise ValueError(
                "Invalid value for os_type. Must be 'linux', 'macos', or 'windows'."
            )

        return values

    # @field_validator("parameters")
    # def validate_parameters(cls, v):
    #     # required_parameters_fields = ["flags", "fingerprint"]
    #     # for field in required_parameters_fields:
    #     #     if field not in v:
    #     #         raise ValueError(f"Missing required field in parameters: {field}")
    #     #
    #     # required_flags_fields = [
    #     #     "audio_masking",
    #     #     "fonts_masking",
    #     #     "geolocation_masking",
    #     #     "geolocation_popup",
    #     #     "graphics_masking",
    #     #     "graphics_noise",
    #     #     "localization_masking",
    #     #     "media_devices_masking",
    #     #     "navigator_masking",
    #     #     "ports_masking",
    #     #     "proxy_masking",
    #     #     "screen_masking",
    #     #     "timezone_masking",
    #     #     "webrtc_masking",
    #     # ]
    #     # for field in required_flags_fields:
    #     #     if field not in v["flags"]:
    #     #         raise ValueError(f"Missing required field in parameters.flags: {field}")
    #
    #     parameters_to_fingerprint = {
    #         "audio_masking": "audio",
    #         "fonts_masking": "fonts",
    #         "geolocation_masking": "geolocation",
    #         "graphics_masking": "graphic",
    #         "localization_masking": "localization",
    #         "media_devices_masking": "media_devices",
    #         "navigator_masking": "navigator",
    #         "ports_masking": "ports",
    #         "screen_masking": "screen",
    #         "timezone_masking": "timezone",
    #         "webrtc_masking": "webrtc",
    #     }
    #
    #     for key, value in v.__dict__.items():
    #         if value == "custom":
    #             lookup = parameters_to_fingerprint.get(key, None)
    #             if lookup is None:
    #                 continue
    #             if lookup not in v["fingerprint"]:
    #                 raise ValueError(
    #                     f"You must define {lookup} in parameters.fingerprint since {key} is set to 'custom'"
    #                 )
    #
    #     # Test proxy_masking
    #     if values["flags"]["proxy_masking"] == "custom":
    #         if not values["proxy"]:
    #             raise ValueError(
    #                 "Missing required $.proxy field 'proxy_masking' set to 'custom'."
    #             )
    #     return v
