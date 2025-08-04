from pydantic import BaseModel
from typing import Optional, Literal

class AnalyticsEvent(BaseModel):
    type: Literal[
        "page_view", 
        "click", 
        "scroll_depth", 
        "user_agent", 
        "session_duration"
    ]
    path: str
    timestamp: str  # Can optionally validate ISO later
    element: Optional[str] = None
    element_id: Optional[str] = None
    class_name: Optional[str] = None
    max_scroll: Optional[int] = None
    user_agent: Optional[str] = None
    duration_ms: Optional[int] = None
