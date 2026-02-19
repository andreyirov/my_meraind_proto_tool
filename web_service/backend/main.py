from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

# Import the LLM function
try:
    from llm import generate_diagram_code
except ImportError:
    # If running from root, adjust path
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from llm import generate_diagram_code

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Optional

class DiagramRequest(BaseModel):
    diagram_type: str
    description: str
    current_diagram: Optional[str] = None

@app.post("/api/generate")
async def generate(request: DiagramRequest):
    try:
        code = generate_diagram_code(request.diagram_type, request.description, request.current_diagram)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve frontend static files
# Assuming frontend is in ../frontend relative to this file
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend directory not found at {frontend_path}")
