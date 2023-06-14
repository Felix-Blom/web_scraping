from time import sleep

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
specialisations[3].click()


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

try:
    myElem = WebDriverWait(d, delay).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='cell cell--name']"))
    )
    data_entries = d.find_elements(By.XPATH, "//button[@class='cell cell--name']")
    y_position = 0
    for i, entry in enumerate(data_entries):
        while not entry.is_displayed():
            d.execute_script("arguments[0].scrollIntoView();", entry)
            sleep(1)
        actions.move_to_element(entry).perform()
        entry.click()
        print(f"{i}:{entry.text}")
        entry.click()
        sleep(3)
        

except TimeoutException:
    print("Loading took too much time!")


# print(d[0])
while True:
    pass
