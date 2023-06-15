from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException

 
service = ChromeService(executable_path="C:\webdrivers\chromedriver.exe")
d = webdriver.Chrome(service=service)

d.get(
    "https://www.cbr.nl/nl/rijbewijs-houden/nl/gezondheidsverklaring/zoek-een-specialist.htm"
)

"""Set Location to Amsterdam"""
location = d.find_element(
    By.XPATH, "//input[@id='specialists__selector__location-input']"
)
location.send_keys("Amsterdam")

location.send_keys(Keys.ARROW_DOWN)
location.send_keys(Keys.ENTER)

"""Set specialisation to something"""
# Select the correct specialisation
specialisation_button = d.find_element(
    By.XPATH, "//button[@id='specialists__selector__specialism-button']"
)
specialisation_button.click()

specialisations = d.find_elements(By.CLASS_NAME, "specialism__option")
SPECIALIZATION = specialisations[3].text
specialisations[0].click()


"""Change distance to Heel Nederland"""
afstand_button = d.find_element(
    By.XPATH, "//button[@id='specialists__selector__distance-button']"
)
afstand_button.click()

# Select Heel Nederland
afstand = d.find_elements(By.CLASS_NAME, "distance")

afstanden = d.find_elements(By.CLASS_NAME, "distance__option")
afstanden[3].click()
# afstand[0].click()

delay = 10  # seconds
actions = ActionChains(d)

LOCATIES = []
TEL_NUMBERS = []
ADRESSEN = []


try:
    myElem = WebDriverWait(d, delay).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='cell cell--name']"))
    )
    data_entries = d.find_elements(By.XPATH, "//button[@class='cell cell--name']")
    for i, entry in enumerate(data_entries):
        if i is len(data_entries) - 1:
            break
        try:
            d.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", entry)
            actions.move_to_element(entry).perform()
            entry.click()
            LOCATIE = entry.text
            LOCATIES.append(LOCATIE)
            
            try:
                # Wait for information to load    
                myElem = WebDriverWait(d, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "details__contact__phone")))
                

                TEL_NUMBER = d.find_element(By.CLASS_NAME, "details__contact__phone").get_attribute("href").replace("tel:", "")
                TEL_NUMBERS.append(TEL_NUMBER)

                ADRES = d.find_element(By.XPATH, "//div[@class='details__gridcol']//p").get_attribute("textContent")
                ADRESSEN.append(ADRES)
                print(f"Iteratie {i}, Locatie: {LOCATIE}, Adres: {ADRES}, TelNR: {TEL_NUMBER}")
                entry.click()
                sleep(2)
            except TimeoutException:
                print("Loading information took too much time!")
            
        except MoveTargetOutOfBoundsException:
            print(f"Unable to scroll to entry {i}")

except TimeoutException:
    print("Loading took too much time!")


print(f"Loc: {len(LOCATIES)}, Tel: {len(TEL_NUMBERS)}, Adres: {len(ADRESSEN)}")

data = {
    'Locatie': LOCATIES,
    'Tel_nummer': TEL_NUMBERS,
    "Adres": ADRESSEN
}

df = pd.DataFrame(data)

# Do this on the first run as we need to make the file
df.to_excel("cbr_info.xlsx", index=False, sheet_name=SPECIALIZATION)
# print(d[0])
while True:
    pass
