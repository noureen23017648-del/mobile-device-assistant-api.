from app.schemas.device import Device


device = Device(
    brand="Samsung",
    model="Galaxy S24 Ultra",
    specs={
        "display": "6.8 inch Dynamic AMOLED",
        "battery": "5000 mAh",
        "camera": "200MP"
    },
    release_year=2024,
    price_tier="flagship"
)

print(device)
print(device.model_dump())
