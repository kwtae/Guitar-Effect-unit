from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime

class PresetCreate(BaseModel):
    user_id: str
    preset_name: str
    ai_target_prompt: str
    parameters: Dict[str, Any] = Field(description="Dynamic parameters like drive, delay, routing matrix")
    input_features: Optional[Dict[str, Any]] = None
    is_public: bool = False

class PresetResponse(PresetCreate):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class RLHFFeedbackCreate(BaseModel):
    user_id: str
    preset_id: str
    rating: int = Field(ge=1, le=5, description="1 to 5 user rating of AI tone")
    adjusted_parameters: Dict[str, Any] = Field(description="The user's manual adjustments over AI suggestion")

class RLHFFeedbackResponse(RLHFFeedbackCreate):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True
