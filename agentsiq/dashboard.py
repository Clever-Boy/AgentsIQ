from fastapi import FastAPI
from fastapi.responses import JSONResponse, PlainTextResponse
import os, glob

app = FastAPI(title="AgentsIQ Dashboard")

@app.get("/logs")
def logs():
    files = sorted(glob.glob("logs/*.jsonl"))
    if not files:
        return JSONResponse({"message": "No logs yet."})
    latest = files[-1]
    with open(latest, "r", encoding="utf-8") as f:
        return PlainTextResponse(f.read(), media_type="text/plain")

@app.get("/metrics")
def metrics():
    path = "agentops_records/metrics.csv"
    if not os.path.exists(path):
        return JSONResponse({"message": "No metrics yet."})
    with open(path, "r", encoding="utf-8") as f:
        return PlainTextResponse(f.read(), media_type="text/plain")
