from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

needs = []
volunteers = []

@app.get("/")
def home():
    return {"message": "SmartAid AI backend running"}

# ADD NEED
@app.post("/add_need")
def add_need(data: dict):
    needs.append(data)
    return {"message": "Need added"}

# ADD VOLUNTEER
@app.post("/add_volunteer")
def add_volunteer(data: dict):
    volunteers.append(data)
    return {"message": "Volunteer added"}

# SMART MATCHING
@app.get("/match")
def match():
    results = []

    for need in needs:
        for vol in volunteers:
            score = 0

            # Location match
            if need["location"].lower() == vol["location"].lower():
                score += 40

            # Skill match
            if need["skill"].lower() == vol["skill"].lower():
                score += 40

            # Priority weight
            if need["priority"] == "high":
                score += 30
            elif need["priority"] == "medium":
                score += 20
            else:
                score += 10

            # Availability
            if vol["availability"] == "yes":
                score += 20

            results.append({
                "need": need["title"],
                "priority": need["priority"],
                "volunteer": vol["name"],
                "availability": vol["availability"],
                "score": score
            })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:3]  # Top 3 matches