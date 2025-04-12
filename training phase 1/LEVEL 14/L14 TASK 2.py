import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
chrome_driver_path = r"C:\Users\HP\OneDrive\Desktop\scraping\chromedriver-win64 (1)\chromedriver-win64\chromedriver.exe"
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
url = 'https://www.cricbuzz.com/cricket-series/3472/indian-premier-league-2021/matches'
driver.get(url)
time.sleep(3) 
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()
matches = soup.find_all('div', class_='cb-col-60 cb-col cb-srs-mtchs-tm')

data = []

for match in matches:
    try:
        match_link = match.find('a', href=True)
        match_href = 'https://www.cricbuzz.com' + match_link['href'] if match_link else ''
        match_name = match_link.text.strip() if match_link else ''

        teams = match.find_all('div', class_='cb-hmscg-tm-nm')
        team1 = teams[0].text.strip() if len(teams) > 0 else ''
        team2 = teams[1].text.strip() if len(teams) > 1 else ''

        date_div = match.find_next('div', class_='cb-col cb-col-100 cb-srs-mtchs-tm-dt')
        match_datetime_start = date_div.text.strip() if date_div else ''

        venue_div = match.find_next('div', class_='cb-col cb-col-100 cb-srs-mtchs-tm-vnu')
        match_venue = venue_div.text.strip() if venue_div else ''

        match_no_div = match.find_previous('h2')
        match_no = match_no_div.text.strip() if match_no_div else ''

       
        row = {
            'year': '2021',
            'series_type': 'T20',
            'series_name': 'Indian Premier League 2021',
            'match_no': match_no,
            'match_type': 'League',
            'match_name': match_name,
            'match_href': match_href,
            'match_team1': team1,
            'match_team2': team2,
            'match_datetime_start': match_datetime_start,
            'match_date_end': match_datetime_start,
            'match_venue': match_venue
        }
        data.append(row)
    except Exception as e:
        print(f"Error processing match: {e}")

df = pd.DataFrame(data)
df.to_csv('ipl_2021_matches.csv', index=False)

print(df.head())
print("Data scraped and saved successfully!")
