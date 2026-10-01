
from fastapi import FastAPI, HTTPException

from app.schemas.device import Device
from app.services.extraction import extract_device


app = FastAPI(
    title="Mobile Device Assistant API",
    description="AI-powered Mobile Device Assistant",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Mobile Device Assistant API is running"
    }


@app.post("/device-assistant")
def device_assistant(device: Device):

    try:
        device_text = f"""
        Brand: {device.brand}
        Model: {device.model}
        Specifications: {device.specs}
        Release Year: {device.release_year}
        Price Tier: {device.price_tier}
        """

        extracted_device = extract_device(device_text)

        return {
            "device": extracted_device.model,
            "brand": extracted_device.brand,
            "specs": extracted_device.specs,
            "release_year": extracted_device.release_year,
            "price_tier": extracted_device.price_tier
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing device: {str(e)}"
        )

