from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import requests
import sys
import base64
import json
import os


state = ""
plate = ""

car_name = ""
msrp = 0



def find_model():
    global state
    global plate
    global car_name

    url = "https://findbyplate.com/US/"+state+"/"+plate+"/"
    print("URL: "+url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    carname = soup.find_all(class_="vehicle-modal")

    car_name = carname[0].get_text()

    print(car_name+"F")

    get_msrp()

def get_msrp():
    global msrp
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Cars').get_worksheet(1)

    info = car_name.split(' ')

    if len(info) == 4:
        info[2] = info[2]+ " "+info[3]
        info.pop(3)


    for i in info:
        print(i)

    cars = sheet.findall(info[1])
    
    for f in cars:
        rows = f.row
        if sheet.cell(rows,1).value.lower() == info[1].lower():
            if sheet.cell(rows,3).value.lower() == info[0].lower():
                msrp = sheet.cell(f.row, 16).value
                print(msrp)
                break
    save_data()

def save_data():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    info = car_name.split(' ')

    if len(info) == 4:
        info[2] = info[2]+ " "+info[3]
        info.pop(3)

    sheet = client.open('Cars').sheet1

    pp = pprint.PrettyPrinter()
    result = sheet.append_row([info[1], info[2], info[0], msrp, plate, state])
    pp.pprint(result)


def get_plate():
    global plate
    global state
    
    IMAGE_PATH = 'test.jpg'
    SECRET_KEY = 'sk_12bac89cf5b2708ed2c92944'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)

    data = json.loads(json.dumps(r.json()))

    plate = data["results"][0]["plate"]
    state = data["results"][0]["region"]

    print("Plate: "+plate+" State: " + state)

    find_model()
    


def main():
    get_plate()

main()
