
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse,HTMLResponse,PlainTextResponse
import os,glob,html
from .agentops_metrics import summary_by_agent
from .decision_store import latest_decisions

app=FastAPI(title="AgentsIQ Dashboard")

@app.get("/")
def root():
    return HTMLResponse("""
<html><head><title>AgentsIQ Dashboard</title></head>
<body style='font-family:system-ui,sans-serif;padding:1rem'>
<h1>AgentsIQ Dashboard</h1>
<ul>
  <li><a href='/summary'>/summary</a> — Per-agent performance (JSON)</li>
  <li><a href='/decisions'>/decisions</a> — Routing decisions (HTML)</li>
  <li><a href='/decisions.json'>/decisions.json</a> — Decisions (JSON)</li>
  <li><a href='/logs'>/logs</a> — Raw explainability</li>
  <li><a href='/metrics'>/metrics</a> — Raw metrics CSV</li>
</ul>
</body></html>
""")

@app.get("/summary")
def summary():
    return JSONResponse(summary_by_agent())

@app.get("/decisions.json")
def decisions_json(n: int = 20):
    return JSONResponse(latest_decisions(n))

@app.get("/decisions")
def decisions(n: int = 20):
    rows = latest_decisions(n)
    def cell(v):
        if v is None: return ""
        s = html.escape(str(v))
        return s[:160] + ("…" if len(s)>160 else "")
    # Build HTML table
    html_rows = []
    for r in rows[::-1]:  # newest first
        chosen = r.get("chosen")
        strategy = r.get("strategy")
        agent = r.get("agent")
        traits = r.get("traits", {})
        est_cost = r.get("est_cost_chosen")
        saved_next = r.get("est_cost_saved_vs_next_best")
        saved_gpt4 = r.get("est_cost_saved_vs_gpt4o")
        tokens = r.get("tokens_total_est")
        # top3
        scored = r.get("scored", [])[:3]
        top_details = "<br>".join([f"{i+1}. {cell(s.get('model'))} (score={round(s.get('score',0),3)}, est_cost=${s.get('est_cost')})" for i,s in enumerate(scored)])
        html_rows.append(f"""
<tr>
<td>{cell(agent)}</td>
<td>{cell(strategy)}</td>
<td><b>{cell(chosen)}</b></td>
<td>${cell(est_cost)}</td>
<td>${cell(saved_next)}</td>
<td>${cell(saved_gpt4)}</td>
<td>{cell(tokens)}</td>
<td>{top_details}</td>
<td title='{cell(r.get('task'))}'>{cell(r.get('task'))}</td>
</tr>
""")
    page = """
<html><head><title>AgentsIQ Decisions</title>
<style>
table{border-collapse:collapse;width:100%%}th,td{border:1px solid #ddd;padding:8px}th{background:#f5f5f5;text-align:left}
</style></head>
<body style='font-family:system-ui,sans-serif;padding:1rem'>
<h2>Routing Decisions (newest first)</h2>
<table>
<thead><tr><th>Agent</th><th>Strategy</th><th>Chosen</th><th>Est Cost</th><th>Saved vs Next</th><th>Saved vs GPT-4o</th><th>Est Tokens</th><th>Top Candidates</th><th>Task (preview)</th></tr></thead>
<tbody>
%s
</tbody></table>
<p style='color:#666'>Estimates are based on configurable per-1k token costs and simple token heuristics.</p>
</body></html>
""" % ("".join(html_rows) or "<tr><td colspan='9'>No decisions yet.</td></tr>")
    return HTMLResponse(page)

@app.get("/logs")
def logs():
    files=sorted(glob.glob("logs/*.jsonl"))
    if not files: return JSONResponse({"message":"No logs yet."})
    latest=files[-1]
    with open(latest,"r",encoding="utf-8") as f:
        return PlainTextResponse(f.read(),media_type="text/plain")

@app.get("/metrics")
def metrics():
    path="agentops_records/metrics.csv"
    if not os.path.exists(path): return JSONResponse({"message":"No metrics yet."})
    with open(path,"r",encoding="utf-8") as f: 
        return PlainTextResponse(f.read(),media_type="text/plain")
