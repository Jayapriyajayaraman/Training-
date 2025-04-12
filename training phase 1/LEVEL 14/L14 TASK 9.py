from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define the data model
class PlayerStats(BaseModel):
    player_name: str
    team: str
    matches_played: int
    total_runs: int
    average_score: float

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Hello World"}

# Player endpoint
@app.post("/player/")
def create_player(player: PlayerStats):
    return player
