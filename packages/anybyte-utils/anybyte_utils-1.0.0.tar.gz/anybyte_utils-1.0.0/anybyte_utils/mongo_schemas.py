from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
from datetime import datetime, timezone


class MouseMovement(BaseModel):
    timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())
    position: Tuple[int, int] = Field(
        ..., example=(100, 200)
    )  # presumably in pixels - idk how you want to denote position


class Keystroke(BaseModel):
    timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())
    key: str = Field(..., example="a")


class MouseClick(BaseModel):
    timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())
    position: Tuple[int, int] = Field(
        ..., example=(150, 250)
    )  # presumably in pixels - idk how you want to denote position
    button: str = Field(..., example="left")


class MouseScroll(BaseModel):
    timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())
    speed: float = Field(
        ..., example=(150, 250)
    )  # presumably in pixels - idk how you want to denote position
    direction: str = Field(..., example="up")


class CaptchaHitSchema(BaseModel):
    api_key: str = Field(
        ..., example="abc1234"
    )  # this is the id of the client for whom the captcha is getting fulfilled - i.e. the business buying the data
    mouse_movements: List[MouseMovement] = Field(..., example=[])
    mouse_clicks: List[MouseClick] = Field(..., example=[])
    keystrokes: List[Keystroke] = Field(..., example=[])
    scroll_movements: List[MouseScroll] = Field(..., example=[])
    served_img_keys: List[str] = Field(..., example=["testS3key", "testS3key2"])
    selected_box_ids: List[int] = Field(..., example=[1, 2, 3])
    suspicious_request: bool = Field(..., example=True)
    captcha_verification_success: bool = Field(..., example=True)
    completion_duration: float = Field(..., exmaple=120201.1)  # in milliseconds
    iso_timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())


class UserInteractionUpdate(BaseModel):
    captcha_client_id: Optional[str] = (
        None  # this is the id of the client for whom the captcha is getting fulfilled - i.e. the business buying the data
    )
    session_id: Optional[str] = None
    served_img_id: Optional[str] = None
    mouse_movements: Optional[List[MouseMovement]] = None
    mouse_clicks: Optional[List[MouseClick]] = None
    keystrokes: Optional[List[Keystroke]] = None
    scroll_movements: Optional[List[MouseScroll]] = None
    client_response: Optional[str] = None
    captcha_success: Optional[bool] = None
    completion_duration: Optional[float] = None
    timestamp: Optional[datetime] = None


class PlatformSchema(BaseModel):
    api_key: str = Field(..., example="abc123")
    user_platform: str = Field(..., example="desktop")  # or "mobile"
    ip_address: str = Field(..., example="1.1.1.1")
    confidence_score: float = Field(..., example="0.01")
    suspicious_request: bool = Field(..., example=True)
    served_img_keys: List[str] = Field(..., example=["abc123", "abc1232"])
    selected_box_ids: List[int] = Field(..., example=[1, 2, 3])
    captcha_verification_success: bool = Field(..., example=True)


class MouseMovement(BaseModel):
    timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())
    position: Tuple[int, int] = Field(
        ..., example=(100, 200)
    )  # presumably in pixels - idk how you want to denote position


class MLSchemaDesktop(BaseModel):
    mouse_movements: List[MouseMovement] = Field(..., example=[])


class MouseScroll(BaseModel):
    timestamp: datetime = Field(..., example=datetime.now(timezone.utc).isoformat())
    speed: float = Field(
        ..., example=(150, 250)
    )  # presumably in pixels - idk how you want to denote position
    direction: str = Field(..., example="up")


class MLSchemaMobile(BaseModel):
    mouse_scroll_movements: List[MouseScroll] = Field(..., example=[])
