import base64
import json
import tkinter as tk
from tkinter import filedialog
import requests
import plate.py


IMAGE_PATH = test.jpg
SECRET_KEY = 'sk_12bac89cf5b2708ed2c92944'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)


with open(r.json(), 'r') as f:
    datastore = json.load(f)

plate = datastore["results"][0]["plate"]
region = datastore["results"][0]["region"]

plate.find_model(region,plate)

