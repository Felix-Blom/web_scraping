from time import sleep
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from name_remapping import name_remap

class CBRscraper:
    def __init__(self, driver: webdriver, weburl: str):
        # Initialize empty lists
        self.locaties = []
        self.tel_numbers = []
        self.adressen = []
        self.emails = []

        # Initialize connection with url
        self.driver = driver
        self.weburl = weburl
        self.load_url()


    def load_url(self):
        """Initialize connection to website"""
        self.driver.get(self.weburl)
   

    def set_location(self, selected_location: str  = "Amsterdam"):
        """Set the location to Amsterdam"""
        self.location = self.driver.find_element(
            By.XPATH, "//input[@id='specialists__selector__location-input']"
        )   

        self.location.send_keys(selected_location)
        self.location.send_keys(Keys.ARROW_DOWN)
        self.location.send_keys(Keys.ENTER)

    def set_distance(self, selected_distance: int = 3):
        """Set the distance to all if it's 3"""
        # Find all distances button
        distances_button = self.driver.find_element(
            By.XPATH, "//button[@id='specialists__selector__distance-button']"
        )
        distances_button.click()

        # Select the  distance (3 = all of NL)
        afstanden = self.driver.find_elements(By.CLASS_NAME, "distance__option")
        afstanden[selected_distance].click()
        sleep(5)

    def set_specialization(self, spec_iter: int) -> str:
        """Set the specialization to the current specialization as we loop over all"""
        # Find all specializations button
        specialisation_button = self.driver.find_element(
            By.XPATH, "//button[@id='specialists__selector__specialism-button']"
        )
        specialisation_button.click()

        # Find all specializations and click the current one
        specialisations = self.driver.find_elements(By.CLASS_NAME, "specialism__option")
        specialisations[spec_iter].click()
        
        # Return text of current specializtion & rename it if the text is too long 
        SPECIALIZATION_TEXT = specialisations[spec_iter].text
        self.output_name = SPECIALIZATION_TEXT if spec_iter not in name_remap else name_remap[spec_iter]

    
    def scrape_data(self):
        """Scrapes the data after the functions above initalized the current page"""
        try:
            my_elem = WebDriverWait(self.driver, self.delay).until(
                EC.presence_of_element_located((By.XPATH, "//button[@class='cell cell--name']"))
            )
            data_entries = self.driver.find_elements(By.XPATH, "//button[@class='cell cell--name']")
            actions = ActionChains(self.driver)
            
            for i, entry in enumerate(data_entries):
                if i == len(data_entries) - 1:
                    break
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", entry)
                    actions.move_to_element(entry).perform()
                    entry.click()
                    locatie = entry.text
                    
                    # Get all the other information of the entry
                    self.get_information(locatie, i)

                    entry.click() # Close entry
                    sleep(3) # Wait for page to close

                except MoveTargetOutOfBoundsException:
                    print(f"Unable to scroll to entry {i}")

            
        except TimeoutException:
            print("Loading took too much time!")


    def get_information(self, locatie: str, iteration: int):
        tel_number = self.extract_tel_number()
        adres = self.extract_adres()
        email = self.extract_email()

        self.locaties.append(locatie)
        self.adressen.append(adres)
        self.tel_numbers.append(tel_number)
        self.emails.append(email)

        # Print current information
        print(f"Iteratie {iteration}, Locatie: {locatie}, Adres: {adres}, TelNR: {tel_number}, Mail: {email}")


    def extract_tel_number(self, patience: int = 0.5) -> str:
        try:
            my_elem = WebDriverWait(self.driver, patience).until(
                EC.presence_of_element_located((By.CLASS_NAME, "details__contact__phone")))
            tel_number = self.driver.find_element(By.CLASS_NAME, "details__contact__phone").get_attribute("href").replace("tel:", "")
        except TimeoutException:
            tel_number = "Not available"
        
        return tel_number

    def extract_adres(self, patience: int = 0.5) -> str:
        try:
            my_elem = WebDriverWait(self.driver, patience).until(EC.presence_of_element_located((By.XPATH, "//div[@class='details__gridcol']//p")))
            adres = self.driver.find_element(By.XPATH, "//div[@class='details__gridcol']//p").get_attribute("textContent")                  
        except TimeoutException:
            adres = "Not available"
        
        return adres

    def extract_email(self, patience: int = 0.5) -> str:
        try:
            # Await element
            my_elem = WebDriverWait(self.driver, patience).until(EC.presence_of_element_located((By.CLASS_NAME, "details__contact__email")))
            email = self.driver.find_element(By.CLASS_NAME, "details__contact__email").get_attribute("href").replace("mailto:", "")
        except TimeoutException: 
            email = "Not available"
        
        return email

    def create_dataframe(self):
        data = {
            'Locatie': self.locaties,
            'Tel_nummer': self.tel_numbers,
            "Adres": self.adressen,
            "Email": self.emails
        }

        self.df = pd.DataFrame(data)

    def save_data_csv(self):
        self.df.to_csv(f"/outputs/{self.output_name}.csv", index=False)


    def save_data_excel(self, iter):
        filename = 'cbr_info.xlsx'
        # It's the first iteration we create the dataframe
        if iter == 0:
            # Do this on the first run as we need to make the file
            self.df.to_excel(filename, index=False, sheet_name=self.output_name)

        else:
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer:
                # Write the DataFrame to a new sheet
                self.df.to_excel(writer, sheet_name=self.output_name, index=False)