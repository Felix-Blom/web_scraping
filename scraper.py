from selenium import webdriver


class CBRscraper:
    def __init__(self, driver: webdriver, weburl: str):
        self.driver = driver
        self.weburl = weburl

    def load_website(self):
        """Initialize connection to website"""
        self.driver.get(self.weburl)

    def set_location(self, selected_location: str  = "Amsterdam"):
        """Set the location to Amsterdam"""
        location = d.find_element(
            By.XPATH, "//input[@id='specialists__selector__location-input']"
        )   

        location.send_keys(selected_location)
        pass

    def set_distance(self):
        """Set the distance to all if it's 3"""
        pass

    def set_specialization(self, iter):
        pass


    
"""Set Location to Amsterdam"""



location.send_keys(Keys.ARROW_DOWN)
location.send_keys(Keys.ENTER)

"""Set specialisation to current specialization"""
SPEC_ITER = 15
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