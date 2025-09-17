# AgentIQ 🧠🤖
A lightweight multi-agent orchestration framework for **intelligent agents** with:
- 🔀 Hybrid LLM routing (GPT-4, Claude, Gemini, etc.)
- 📊 Explainability & decision logs
- 🔒 Role-based governance & tool permissions
- 📈 Integrated with AgentOps for performance tracking

## ✨ Features
- **Hybrid Orchestration** – dynamically routes tasks to the best LLM based on task type, cost, or latency.
- **Explainability Logs** – every agent decision is recorded with reasoning, confidence, and outcomes.
- **Governance** – define which tools each agent can or cannot access.
- **AgentOps Integration** – capture structured performance metrics for audit & analysis.

## 🚀 Quick Start
```bash
git clone https://github.com/yourname/AgentIQ.git
cd AgentIQ
pip install -r requirements.txt
```

Set your API keys as environment variables:
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant..."
export GOOGLE_API_KEY="your-gemini-key"
```

Run the demo:
```bash
python examples/run_demo.py
```

## ⚙️ Configuration
See [`config.yaml`](./config.yaml) to define agents, models, and permissions.

## 📊 Dashboard (Optional)
Start a simple FastAPI dashboard:
```bash
uvicorn agentiq.dashboard:app --reload
```
This will visualize decision traces and AgentOps performance metrics.

## 📜 License
This project is licensed under the MIT License – see [LICENSE](./LICENSE).

---
Built with ❤️ to advance the future of intelligent agents.
