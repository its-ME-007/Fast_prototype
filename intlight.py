from fastapi import FastAPI, HTTPException, APIRouter, Query
from typing import Optional

app = FastAPI()

# Define the status dictionary to keep track of the states
status = {
    "Internal": {
        "RoofLight": {"Status": 0, "Brightness": 0},
        "DoorPuddleLights": {"Status": 0, "Brightness": 0},
        "FloorLights": {"Status": 0, "Brightness": 0},
        "DashboardLights": {"Status": 0, "Brightness": 0},
        "BootLights": {"Status": 0}
    }
}

# Define the router
int_lighting_router = APIRouter()

# Define endpoints for setting and getting light statuses and brightness
@int_lighting_router.post('/internal/rooflight/status')
async def set_internal_rooflight_status(Status: int):
    if Status not in [0, 1]:
        raise HTTPException(status_code=400, detail="Invalid Status")
    status["Internal"]["RoofLight"]["Status"] = Status
    return {"RoofLightStatus": status["Internal"]["RoofLight"]["Status"]}

@int_lighting_router.get('/internal/rooflight/status')
async def get_internal_rooflight_status():
    return {"RoofLightStatus": status["Internal"]["RoofLight"]["Status"]}

@int_lighting_router.post('/internal/rooflight/brightness')
async def set_internal_rooflight_brightness(Brightness: int):
    if not 0 <= Brightness <= 100:
        raise HTTPException(status_code=400, detail="Invalid Brightness")
    status["Internal"]["RoofLight"]["Brightness"] = Brightness
    return {"RoofLightBrightness": status["Internal"]["RoofLight"]["Brightness"]}

@int_lighting_router.get('/internal/rooflight/brightness')
async def get_internal_rooflight_brightness():
    return {"RoofLightBrightness": status["Internal"]["RoofLight"]["Brightness"]}

# Similar endpoints for other lights

# Register the router
app.include_router(int_lighting_router)
