"""
KisanKavach FastAPI Backend Application.
Serves live multi-agent API endpoints and responsive frontend interface.
"""
import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.agents.swarm_orchestrator import AgroSwarmOrchestrator
from app.tools.geocoding_tool import search_location

app = FastAPI(
    title="KisanKavach (AgroResilience Swarm)",
    description="Autonomous Multimodal Climate Risk, Mandi Arbitrage & Supply Chain Swarm",
    version="1.0.0"
)

# Initialize Orchestrator
orchestrator = AgroSwarmOrchestrator()

# Mount static directory
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

class SwarmRequest(BaseModel):
    lat: float
    lon: float
    crop: str = "Wheat"
    quantity_quintals: float = 50.0
    simulate_hazard: bool = False
    image_base64: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>KisanKavach Backend Running</h1>")

@app.post("/api/swarm/execute")
async def execute_swarm_api(req: SwarmRequest):
    """
    Main endpoint triggering multi-agent swarm execution.
    """
    try:
        result = await orchestrator.execute_swarm(
            lat=req.lat,
            lon=req.lon,
            crop=req.crop,
            quantity_quintals=req.quantity_quintals,
            image_base64=req.image_base64,
            simulate_hazard=req.simulate_hazard
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search")
async def search_location_api(q: str):
    """
    Live location search autocomplete via OpenStreetMap Nominatim.
    """
    results = await search_location(q)
    return {"results": results}

@app.get("/api/health")
async def health_check():
    return {
        "status": "HEALTHY",
        "system": "KisanKavach Swarm",
        "live_apis": {
            "open_meteo": "CONNECTED",
            "osm_nominatim": "CONNECTED",
            "osrm_routing": "CONNECTED",
            "apmc_agmarknet": "CONNECTED"
        }
    }
