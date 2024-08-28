from fastapi import FastAPI, APIRouter, HTTPException

app = FastAPI()

bms_router = APIRouter()

# Define the status dictionary to keep track of the states
status = {
    "Battery": {
        "Voltage": 0,
        "Current": 0,
        "SOC": 0,
        "NumberOfCells": 0,
        "CellVoltage": 0,
        "ChargingMOSFET": "OFF",
        "DischargingMOSFET": "OFF",
        "CellMinimumVoltage": 0,
        "CellMinVoltageNumber": 0,
        "CellMaximumVoltage": 0,
        "CellMaxVoltageNumber": 0,
        "Capacity": 0,
        "ERRORStatus": 0,
        "Temperature": 0
    }
}

@bms_router.post('/battery/{attribute}/{value}')
async def set_battery_attribute(attribute: str, value: int):
    valid_ranges = {
        "voltage": (0, 100),
        "current": (-500, 500),
        "soc": (0, 100),
        "numberofcells": (0, 40),
        "cellvoltage": (0, 5),
        "cellminimumvoltage": (0, 5),
        "cellminvoltagenumber": (0, 40),
        "cellmaximumvoltage": (0, 5),
        "cellmaxvoltagenumber": (0, 40),
        "capacity": (0, 300),
        "errorstatus": (0, 255),
        "temperature": (0, 100)
    }

    attribute_mapping = {
        "voltage": "Voltage",
        "current": "Current",
        "soc": "SOC",
        "numberofcells": "NumberOfCells",
        "cellvoltage": "CellVoltage",
        "chargingmosfet": "ChargingMOSFET",
        "dischargingmosfet": "DischargingMOSFET",
        "cellminimumvoltage": "CellMinimumVoltage",
        "cellminvoltagenumber": "CellMinVoltageNumber",
        "cellmaximumvoltage": "CellMaximumVoltage",
        "cellmaxvoltagenumber": "CellMaxVoltageNumber",
        "capacity": "Capacity",
        "errorstatus": "ERRORStatus",
        "temperature": "Temperature"
    }

    if attribute not in attribute_mapping:
        raise HTTPException(status_code=400, detail="Invalid attribute")

    if attribute in valid_ranges and not (valid_ranges[attribute][0] <= value <= valid_ranges[attribute][1]):
        raise HTTPException(status_code=400, detail=f"Invalid {attribute} value")
    
    if attribute in ["chargingmosfet", "dischargingmosfet"]:
        status["Battery"][attribute_mapping[attribute]] = "ON" if value == 1 else "OFF"
    else:
        status["Battery"][attribute_mapping[attribute]] = value

    return {"status": f"Battery {attribute} is now {value}"}

@bms_router.get('/battery/{attribute}')
async def get_battery_attribute(attribute: str):
    attribute_mapping = {
        "voltage": "Voltage",
        "current": "Current",
        "soc": "SOC",
        "numberofcells": "NumberOfCells",
        "cellvoltage": "CellVoltage",
        "chargingmosfet": "ChargingMOSFET",
        "dischargingmosfet": "DischargingMOSFET",
        "cellminimumvoltage": "CellMinimumVoltage",
        "cellminvoltagenumber": "CellMinVoltageNumber",
        "cellmaximumvoltage": "CellMaximumVoltage",
        "cellmaxvoltagenumber": "CellMaxVoltageNumber",
        "capacity": "Capacity",
        "errorstatus": "ERRORStatus",
        "temperature": "Temperature"
    }

    if attribute not in attribute_mapping:
        raise HTTPException(status_code=400, detail="Invalid attribute")

    return {attribute_mapping[attribute]: status["Battery"][attribute_mapping[attribute]]}

app.include_router(bms_router)
