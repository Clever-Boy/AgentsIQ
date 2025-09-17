from fastapi import FastAPI
import json
import os

app = FastAPI()

@app.get("/logs")
def get_logs():
    if os.path.exists("logs/decisions.json"):
        with open("logs/decisions.json") as f:
            return json.load(f)
    return {"message": "No logs found"}

@app.get("/metrics")
def get_metrics():
    if os.path.exists("agentops_records/metrics.json"):
        with open("agentops_records/metrics.json") as f:
            return json.load(f)
    return {"message": "No metrics found"}
