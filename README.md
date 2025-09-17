# AgentsIQ 🧠🤖
A lightweight multi-agent orchestration framework with:
- 🔀 Hybrid LLM routing (OpenAI, Anthropic, Gemini)
- 📊 Explainability logs (JSONL traces)
- 🔒 Simple governance (tool permissions)
- 📈 AgentOps-style metrics recorder (CSV + JSON)

## Quick Start
```bash
pip install -r requirements.txt
# copy example env and fill your keys
cp .env.example .env
# run demo
python examples/run_demo.py
# (optional) start dashboard
uvicorn agentsiq.dashboard:app --reload
```

## API Keys
Create a `.env` at project root (copy from `.env.example`).
Keys are auto-loaded by `dotenv` in the router:
```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza-...
```

## Config
See `config.yaml` for example agents and router strategy.

## License
MIT — see LICENSE.
