import gspread
from gspread_formatting import *
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)

sheet = client.open('Shipments').sheet1 #Takes up to 5 seconds to open ( maybe leave it open )
expected_headers = ['NAME', 'Shipping country', 'Destination COUNTRY (CITY)', 'LABEL CREATED DATE', 'Pickup / Drop off date', 'LABEL NUMBER', 'DESCRIPTION', 'STATUS', 'People Working', 'Instructions( for bot )']

python_sheet = sheet.get_all_records(expected_headers=expected_headers)

col = sheet.col_values(10)
to_check = [i+1 for i, x in enumerate(col) if x == 'CHECK']
result = []

for i in range(len(to_check)):
    cell = sheet.cell(to_check[i],6).value
    result.append(cell)

driver = webdriver.Chrome()
driver.get("https://www.ups.com/")
cookies_1 = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[1]/div[1]/div[1]/label')
cookies_1.click()
cookies_2 = driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[1]/div[1]/div[3]/button')
cookies_2.click()

for i in range(len(to_check)):

    driver.get(f"https://www.ups.com/track?loc=en_FR&requester=QUIC&tracknum={result[i]}/trackdetails")
    time.sleep(3)
    div = driver.find_element(By.XPATH,'/html/body/div[4]/div[3]/div/div/div/div/div/main/div/app-root/div/app-track-details/div/div[1]/div/div/div/div/div[1]/div/div/div')
    div_txt = div.text

    if "Cancelled" in div_txt or "Returned" in div_txt or "Returned To" in div_txt:
        #Annulé ou Retourné
        sheet.format(f"A{to_check[i]}:I{to_check[i]}", {"backgroundColor": { "red": 1, "green": 0.5, "blue": 0}})
        sheet.update_cell(to_check[i],10,'OK')
    elif "Delivered" in div_txt:
        #Délivré
        sheet.format(f"A{to_check[i]}:I{to_check[i]}", {"backgroundColor": { "red": 0.41, "green": 0.65, "blue": 0.3}})
        sheet.update_cell(to_check[i],10,'OK')
    else:
        #En cours
        sheet.format(f"A{to_check[i]}:I{to_check[i]}", {"backgroundColor": { "red": 1, "green": 1, "blue": 0}})
    div_txt = ""
print("END")
