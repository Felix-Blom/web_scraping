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

SPEC_ITER = 12
 
service = ChromeService(executable_path="C:\webdrivers\chromedriver.exe")
d = webdriver.Chrome(service=service)

d.get(
    "https://www.cbr.nl/nl/rijbewijs-houden/nl/gezondheidsverklaring/zoek-een-specialist.htm"
)

sleep(5)

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
SPECIALIZATION = specialisations[SPEC_ITER].text
specialisations[SPEC_ITER].click()


"""Change distance to Heel Nederland"""
afstand_button = d.find_element(
    By.XPATH, "//button[@id='specialists__selector__distance-button']"
)
afstand_button.click()

# Select Heel Nederland
afstand = d.find_elements(By.CLASS_NAME, "distance")

afstanden = d.find_elements(By.CLASS_NAME, "distance__option")
afstanden[3].click()
sleep(5)
# afstand[0].click()

delay = 2  # seconds
actions = ActionChains(d)

LOCATIES = []
TEL_NUMBERS = []
ADRESSEN = []
EMAILS= []


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
            """TEL NUMBER"""
            try:
                # Wait for information to load    
                myElem = WebDriverWait(d, delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "details__contact__phone")))
                TEL_NUMBER = d.find_element(By.CLASS_NAME, "details__contact__phone").get_attribute("href").replace("tel:", "")
            except TimeoutException:
                TEL_NUMBER = "Not available"

            """ADRES"""
            try:
                # Wait for information to load    
                myElem = WebDriverWait(d, 2).until(EC.presence_of_element_located((By.XPATH, "//div[@class='details__gridcol']//p")))
                ADRES = d.find_element(By.XPATH, "//div[@class='details__gridcol']//p").get_attribute("textContent")                  
            except TimeoutException:
                ADRES = "Not available"

            """EMAIL"""
            try:
                myElem = WebDriverWait(d, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "details__contact__email")))
                EMAIL = d.find_element(By.CLASS_NAME, "details__contact__email").get_attribute("href").replace("mailto:", "")
                
            except TimeoutException: 
                EMAIL = "Not available"
            
            LOCATIES.append(LOCATIE)
            ADRESSEN.append(ADRES)
            TEL_NUMBERS.append(TEL_NUMBER)
            EMAILS.append(EMAIL)
            entry.click()
            sleep(3)

        except MoveTargetOutOfBoundsException:
            print(f"Unable to scroll to entry {i}")

        print(f"Iteratie {i}, Locatie: {LOCATIE}, Adres: {ADRES}, TelNR: {TEL_NUMBER}, Mail: {EMAIL}")

except TimeoutException:
    print("Loading took too much time!")


print(f"Loc: {len(LOCATIES)}, Tel: {len(TEL_NUMBERS)}, Adres: {len(ADRESSEN)}")

data = {
    'Locatie': LOCATIES,
    'Tel_nummer': TEL_NUMBERS,
    "Adres": ADRESSEN,
    "Email": EMAILS
}

df = pd.DataFrame(data)


if SPEC_ITER == 12:
    df.to_csv("AHDH_psych.csv", index=False)
else:
    df.to_csv(f"{SPECIALIZATION.replace(' ', '')}.csv", index=False)

if SPEC_ITER == 0:
# Do this on the first run as we need to make the file
    df.to_excel("cbr_info.xlsx", index=False, sheet_name=SPECIALIZATION)
else:
    filename = 'cbr_info.xlsx'
    sheet_name = SPECIALIZATION
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
        # Write the DataFrame to a new sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)
# print(d[0])