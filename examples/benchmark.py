
import time, json, os
from agentsiq.agent import Agent
from agentsiq.swarm import Swarm
from agentsiq.router import ModelRouter
from agentsiq.decision_store import latest_decisions

TASKS = [
    "Summarize the key ideas of retrieval-augmented generation in 5 bullet points.",
    "Write a tiny Python function to reverse a list and explain its complexity.",
    "Give a TL;DR of multi-agent coordination strategies.",
    "Draft a simple regex to capture email addresses and explain edge cases.",
]

def run():
    researcher=Agent("Researcher","Finds information","openai:gpt-4o-mini",["retrieval"])
    analyst=Agent("Analyst","Summarizes info","anthropic:claude-3-haiku",["summarize"])
    router=ModelRouter(strategy="smart")
    swarm=Swarm([researcher,analyst],router,{})
    for t in TASKS:
        _=swarm.run(t)
        time.sleep(0.1)

    # Summarize last N decisions (just a window view)
    decs = latest_decisions(100)
    by_model = {}
    cost_total = 0.0
    saved_vs_gpt4o = 0.0
    for d in decs:
        if d.get("strategy") != "smart": continue
        m = d.get("chosen")
        by_model[m] = by_model.get(m, 0) + 1
        cost_total += float(d.get("est_cost_chosen") or 0.0)
        saved_vs_gpt4o += float(d.get("est_cost_saved_vs_gpt4o") or 0.0)

    print("\nBENCHMARK SUMMARY")
    print("==================")
    print("Model usage:", json.dumps(by_model, indent=2))
    print("Estimated total cost: $%.4f" % cost_total)
    print("Estimated saved vs GPT-4o baseline: $%.4f" % saved_vs_gpt4o)
    print("\nOpen /decisions to inspect the 'why' per task.")

if __name__ == "__main__":
    run()
