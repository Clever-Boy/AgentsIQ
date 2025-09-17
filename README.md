
# AgentsIQ — Cost-Smart Router • “Why” Dashboard • Shared RouterManager • Control Panel

AgentsIQ is an **intelligent multi-model router** that picks the most **cost/latency‑efficient** LLM per task, and shows exactly **why** it chose that model. It comes with a dark dashboard, per‑agent metrics (with sparklines and percentiles), a **shared RouterManager** so the runner and UI use the *same* live router, a simple **Control Panel** to tweak strategy/weights, and optional **AgentOps** tracing.

## Why it’s unique
- **Decision intelligence**: objective function balances **cost, latency, quality** with task-aware tweaks (code/summarize/math).
- **Explainability**: logs a full rationale (normalized scores, est. tokens, est. cost, **savings vs next‑best** & **vs GPT‑4o**).
- **Live control**: adjust strategy/weights on the fly via `/control` without redeploying.
- **Shared router**: `RouterManager` ensures both the runner **and** dashboard operate on the same model router instance in a **single process** (`examples/serve_and_demo.py`).
- **Observability**: dark dashboard with **sparklines**, **p50/p90/p99** bars, raw logs and CSV metrics; AgentOps auto‑init if key present.
- **Config‑first**: override profiles/weights in `config.yaml` — no code edits required.

## Install
```bash
git clone <your repo> AgentsIQ
cd AgentsIQ
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# optional keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY, AGENTOPS_API_KEY
```

## Run (single process with shared router + UI)
```bash
python -m examples.serve_and_demo
# open http://127.0.0.1:8000  → Summary, Decisions, Control, Health
```
> Prefer running server separately? You can still do:
> ```bash
> python -m examples.run_demo
> uvicorn agentsiq.dashboard:app --reload
> ```

## Control Panel (the “tray” UI in your browser)
- **Route strategy**: `smart | cheapest | fastest | hybrid`
- **Weights** sliders: Cost / Latency / Quality
- Changes take effect immediately in this process.

## Key files
- `agentsiq/router.py` — SMART routing + cost/latency/quality scoring
- `agentsiq/router_manager.py` — **singleton** router (shared in‑process)
- `agentsiq/dashboard.py` — **dark** HTML UI, `/control`, `/summary`, `/decisions`
- `agentsiq/agentops_metrics.py` — metrics CSV + percentiles
- `agentsiq/decision_store.py` — decision rationale JSON
- `examples/serve_and_demo.py` — **single‑process** server + demo runner

## Sample HTML chart (from real metrics)
Open **`docs/metrics_demo.html`** locally in your browser — it renders this data with inline SVG sparklines and a dark table:

```json
{
  "Researcher": {
    "calls": 7,
    "avg_latency": 7.43354994910104,
    "avg_confidence": 0.781428571428572,
    "models": {"openai:gpt-4o-mini": 3, "google:gemini-pro": 4},
    "series": [14.05, 21.05, 10.26, 1.74, 2.06, 1.18, 1.69],
    "p50": 2.0557, "p90": 16.8537, "p99": 20.6342
  },
  "Analyst": {
    "calls": 7,
    "avg_latency": 0.2281,
    "avg_confidence": 0.78,
    "models": {"tool:summarize": 2, "anthropic:claude-3-haiku": 1, "google:gemini-pro": 4},
    "series": [0, 0, 1.2955, 0.0757, 0.0778, 0.0690, 0.0789],
    "p50": 0.0757, "p90": 0.5655, "p99": 1.2225
  }
}
```

## Windows console note
If you see `UnicodeEncodeError` from AgentOps (emoji in logs), this project applies a **SafeConsoleFilter** automatically when `AGENTOPS_API_KEY` is set. You can also set `PYTHONUTF8=1` or `PYTHONIOENCODING=utf-8` to allow emojis.

## License
MIT
