from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from scraper import CBRscraper

if __name__ == "__main__":
    # Count from 0
    amount_of_specializations = 15
    for SPEC_ITER in range(amount_of_specializations):
        print("New iteration started")

        # Initialize chrome driver
        service = ChromeService(executable_path="C:\webdrivers\chromedriver.exe")
        d = webdriver.Chrome(service=service)

        # Initialize scraper
        CBR_url = "https://www.cbr.nl/nl/rijbewijs-houden/nl/gezondheidsverklaring/zoek-een-specialist.htm"
        scraper = CBRscraper(driver=d, weblink=CBR_url)
        sleep(5)  # Wait for website to load

        scraper.set_location()  # Defaults to Amsterdam
        scraper.set_specialization(SPEC_ITER)
        scraper.set_distance()  # Defaults to the entire NL

        # Scrape the data
        scraper.scrape_data()

        # Create dataframe and outputs
        scraper.create_dataframe()
        scraper.save_data_csv()
        scraper.save_data_excel()