from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
from services.orchestrator import SolarSystemOrchestrator
from data.schemas.user_input_schemas import UserInput
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Solar System Calculator API",
    description="API for calculating optimal solar system configurations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = SolarSystemOrchestrator()

@app.post("/api/v1/calculate")
async def calculate_solar_system(user_input: UserInput):
    """Calculate optimal solar system configuration"""
    try:
        # Convert Pydantic model to dict
        input_data = user_input.dict()
        
        # Run calculation
        result = orchestrator.calculate_solar_system(input_data)
        
        return result
        
    except Exception as e:
        logger.error(f"API calculation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/components/{component_type}")
async def get_components(component_type: str):
    """Get available components by type"""
    try:
        # **LOAD YOUR COMPONENT DATA HERE**
        from core.utils import load_component_data
        
        components_df = load_component_data(component_type)
        components = components_df.to_dict('records')
        
        return {
            'status': 'success',
            'component_type': component_type,
            'components': components
        }
        
    except Exception as e:
        logger.error(f"Failed to load components: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/appliances")
async def get_appliances():
    """Get available appliances"""
    try:
        # **LOAD YOUR APPLIANCE DATA HERE**
        from core.utils import load_appliance_data
        
        appliances_df = load_appliance_data()
        appliances = appliances_df.to_dict('records')
        
        return {
            'status': 'success',
            'appliances': appliances
        }
        
    except Exception as e:
        logger.error(f"Failed to load appliances: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Solar Calculator API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
