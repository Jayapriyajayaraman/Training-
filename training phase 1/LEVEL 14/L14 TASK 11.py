from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# ✅ Step 1: Live scraping function
def scrape_live_commentary(match_id):
    url = f"https://www.cricbuzz.com/live-cricket-scores/{match_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return [{"message": "Failed to fetch data. Please check the match ID or try again later."}]

    soup = BeautifulSoup(response.text, 'html.parser')
    commentary_list = []

    # ✅ Selector for live commentary (adjust if Cricbuzz changes its structure)
    for item in soup.select('.cb-col.cb-col-100.cb-ltst-wgt-hdr .cb-col.cb-col-90.cb-com-ln'):
        commentary = item.get_text(strip=True)
        commentary_list.append({
            "match_id": match_id,
            "commentary": commentary
        })

    # ✅ If no commentary found
    if not commentary_list:
        return [{"message": "No live commentary found. Match may not have started yet."}]

    return commentary_list

# ✅ Step 2: Endpoint for live commentary
@app.post("/get_live/{match_id}")
def get_live_commentary(match_id: int):
    live_data = scrape_live_commentary(match_id)
    return live_data

# ✅ Optional: Home endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to Live Cricket Commentary API"}

