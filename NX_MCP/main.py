"""FastAPI backend for NXPilot AI"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

app = FastAPI(title="NXPilot AI API", version="0.1.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class NXCommandRequest(BaseModel):
    command: str
    parameters: Optional[Dict[str, Any]] = None

class NXCommandResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

# Mock NX Session for now
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "NXPilot AI API"}

@app.post("/api/command", response_model=NXCommandResponse)
async def execute_nx_command(request: NXCommandRequest):
    """Execute an NX command (mock for now)"""
    try:
        # Mock responses based on command
        if request.command == "create_plate":
            return NXCommandResponse(
                success=True,
                message="Plate created successfully",
                data={"feature_id": "plate_001", "dimensions": request.parameters}
            )
        elif request.command == "prepare_for_manufacturing":
            return NXCommandResponse(
                success=True,
                message="Manufacturing package prepared",
                data={"files": ["plate.stp", "drawing.pdf", "bom.json", "screenshot.png"]}
            )
        elif request.command == "ai_review":
            return NXCommandResponse(
                success=True,
                message="AI design review complete",
                data={
                    "score": 85,
                    "issues": [
                        {"severity": "warning", "message": "Fillet radius too small"},
                        {"severity": "warning", "message": "Hole too close to edge"}
                    ]
                }
            )
        else:
            return NXCommandResponse(
                success=False,
                message=f"Unknown command: {request.command}",
                data=None
            )
    except Exception as e:
        return NXCommandResponse(
            success=False,
            message=str(e),
            data=None
        )

@app.get("/api/tools")
async def list_tools():
    """List all available NX tools"""
    return {
        "tools": [
            {"name": "create_plate", "description": "Create a rectangular plate"},
            {"name": "create_bracket", "description": "Create a bracket"},
            {"name": "create_shaft", "description": "Create a shaft"},
            {"name": "prepare_for_manufacturing", "description": "Prepare design for manufacturing"},
            {"name": "ai_review", "description": "Run AI design review"},
            {"name": "generate_bom", "description": "Generate bill of materials"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
