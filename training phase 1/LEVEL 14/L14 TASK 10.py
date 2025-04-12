from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

# 🔥 Step 1: Put your scraped data here (you can replace this with your actual DataFrame from scraping)
data = {
    "match_id": [1, 1, 2, 2],
    "commentary": [
        "First ball, it's a four!",
        "Second ball, dot ball.",
        "Opening batsman hits a six!",
        "Bowler appeals for LBW, not out."
    ]
}
df = pd.DataFrame(data)

# API Endpoint
@app.get("/get/{match_id}")
def get_commentary(match_id: int):
    # Filter dataframe for the given match_id
    filtered_df = df[df['match_id'] == match_id]
    
    if filtered_df.empty:
        return JSONResponse(content={"message": "No data found for this match ID"}, status_code=404)
    
    # Convert to dictionary and return
    commentary_list = filtered_df.to_dict(orient="records")
    return commentary_list
    