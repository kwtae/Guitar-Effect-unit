from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
import uuid
import sys
import os

from . import models, schemas
from .database import engine, get_db

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Phase 2: OSC Bridge to talk to local JUCE C++ Engine (Zero-Latency)
from pythonosc.udp_client import SimpleUDPClient
import json

# Phase 7: GUI Dashboard Integration
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Setup OSC Client
OSC_JUCE_PORT = 9000
osc_client = SimpleUDPClient("127.0.0.1", OSC_JUCE_PORT)

# Initialize Rate Limiter based on user IP
limiter = Limiter(key_func=get_remote_address)

# Create Tables in DB
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Guitar Pedal - Secure Cloud API")

# Register the slowapi rate limit handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS Middleware - STRICT Policy for Production
app.add_middleware(
    CORSMiddleware,
    # In production, replace "*" with the actual frontend domain, e.g., ["https://aiguitarpedal.com"]
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://aiguitarpedal.com"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"], # Restricting methods
    allow_headers=["*"],
)

@app.get("/")
@limiter.limit("10/minute")
def read_root(request: Request):
    """Serve the React/Glassmorphism Web Dashboard directly from FastAPI"""
    frontend_path = "/app/frontend/index.html"
    
    # Fallback if running outside docker
    if not os.path.exists(frontend_path):
        frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "index.html")
        
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"status": "ok", "service": "Backend is running, but UI files were not found."}

@app.post("/presets/", response_model=schemas.PresetResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def create_preset(request: Request, preset: schemas.PresetCreate, db: Session = Depends(get_db)):
    """Create a new AI-generated preset mapping (Rate Limited) & Push to DSP Engine"""
    new_preset_id = str(uuid.uuid4())
    db_preset = models.Preset(**preset.model_dump(), id=new_preset_id)
    db.add(db_preset)
    db.commit()
    db.refresh(db_preset)
    
    # --- OSC Bridge: Push the newly generated AI JSON mapping straight to the C++ Engine ---
    try:
        # We send the entire JSON routing chain string over OSC to the C++ parser
        osc_payload = json.dumps({
            "routing_chain": db_preset.parameters.get("routing", []),
            "dsp_parameters": db_preset.parameters
        })
        osc_client.send_message("/pedal/ai_rebuild_chain", osc_payload)
        print(f"🎸⚡ OSC Payload fired to DSP Engine for Preset: {db_preset.preset_name}")
    except Exception as e:
        print(f"⚠️ Failed to send OSC message to DSP Engine: {e}")
        
    return db_preset

@app.get("/presets/", response_model=List[schemas.PresetResponse])
def get_all_presets(db: Session = Depends(get_db)):
    """Get all presets (Community feature for App Loading)"""
    return db.query(models.Preset).order_by(models.Preset.created_at.desc()).all()

@app.get("/presets/{preset_id}", response_model=schemas.PresetResponse)
def read_preset(preset_id: str, db: Session = Depends(get_db)):
    """Get a specific preset for the Pedal to download"""
    preset = db.query(models.Preset).filter(models.Preset.id == preset_id).first()
    if preset is None:
        raise HTTPException(status_code=404, detail="Preset not found")
    return preset

@app.post("/rlhf-feedback/", response_model=schemas.RLHFFeedbackResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
def submit_rlhf_feedback(request: Request, feedback: schemas.RLHFFeedbackCreate, db: Session = Depends(get_db)):
    """Log user manual adjustments for Reinforcement Learning to fine-tune AI (Rate Limited)"""
    new_feedback_id = str(uuid.uuid4())
    db_feedback = models.RLHFFeedback(**feedback.model_dump(), id=new_feedback_id)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
