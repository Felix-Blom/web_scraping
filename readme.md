# CBR Scraper
CBR uses html that conditionally comes onto the page.
This script loops over the specializations that are in the CBR website and saves certain information (Tel_nr, email, adres).

## Data Privacy
All of the data that is scraped in this project is avaialble for the public and can be found on the CBRWEBSITE(https://www.cbr.nl/nl/rijbewijs-houden/nl/gezondheidsverklaring/zoek-een-specialist.htm)
The data does not belong to me and this project was for studying purposes only. This dataset was chosen as the HTML dynamicly loads in and no JSON file was immediatly available, so it proved to be a bit more challenging. 

## Usage
Install a conda environment using the environment.yaml & run main.py

## Pipeline
The current pipeline loops over the specializations. Most of the information is store in scraper.py

1. Connect with chromewebdriver and connect to url
2. Set the location, specialization and distance
3. Loop over all the data entries and scrape the necessary data
4. Save the data to files

Note. Name remapping changes certain output names, since some of them were incompatible with excel's sheetnaming conventions.
Note2. All of this data is available to the public already by

