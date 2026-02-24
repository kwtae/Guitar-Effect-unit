from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Preset(Base):
    __tablename__ = "presets"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    preset_name = Column(String, index=True)
    ai_target_prompt = Column(String)
    
    # Store DSP Routing and Knobs dynamically
    parameters = Column(JSON) 
    # Store MFCC and Centroid values from the mobile app
    input_features = Column(JSON)
    
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RLHFFeedback(Base):
    __tablename__ = "rlhf_feedback"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    preset_id = Column(String, ForeignKey("presets.id"))
    
    # Rating 1-5 (User feedback)
    rating = Column(Integer)
    # The actual user-tweaked final knob values (to diff with 'parameters')
    adjusted_parameters = Column(JSON)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
