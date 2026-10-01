from app.services.extraction import extract_device


text = """
I got this new Samsung Galaxy S24 Ultra.
It is a flagship phone released in 2024.
It has a 6.8 inch Dynamic AMOLED display,
5000 mAh battery and a 200MP camera.
"""


device = extract_device(text)

print(device)
print()
print(device.model_dump())