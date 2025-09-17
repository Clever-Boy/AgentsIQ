
# AgentsIQ — SMART Router + Why Dashboard
**Differentiator:** Picks the most cost/latency-efficient model per task and **explains why**.

## Run
```bash
pip install -r requirements.txt
python -m examples.run_demo
# optional: run benchmark
python -m examples.benchmark
# dashboard
uvicorn agentsiq.dashboard:app --reload
# open http://127.0.0.1:8000/decisions  (HTML table with cost & savings)
# open http://127.0.0.1:8000/summary    (agent metrics)
```
