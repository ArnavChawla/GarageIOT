from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import requests
import sys

state = ""
plate = ""

car_name = ""
msrp = 0



def find_model(stat,plat):
    global state
    global plate

    state = stat
    plate = plat
    
    url = "https://findbyplate.com/US/"+state+"/"+plate+"/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    carname = soup.find_all(class_="vehicle-modal")

    global car_name

    car_name = carname[0].get_text()

    get_msrp()

def get_msrp():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open('Cars').get_worksheet(1)

    info = car_name.split(' ')

    for i in info:
        print(i)

    porsches = sheet.findall('Macan')


    global msrp

    for f in porsches:
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

    sheet = client.open('Cars').sheet1

    pp = pprint.PrettyPrinter()
    result = sheet.append_row([info[1], info[2], info[0], msrp, plate, state])
    pp.pprint(result)


find_model()

