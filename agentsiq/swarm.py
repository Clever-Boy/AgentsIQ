from typing import List, Dict, Callable
from .agent import Agent
from .router import ModelRouter
from .agentops import record_metrics

class Swarm:
    def __init__(self, agents: List[Agent], router: ModelRouter = None, tools: Dict[str, Callable] = None):
        self.agents = agents
        self.router = router or ModelRouter()
        self.tools = tools or {}

    def run(self, task: str, mode: str = "sequential"):
        results = []
        for agent in self.agents:
            entry = agent.act(task, router=self.router, tools=self.tools)
            record_metrics(entry, note=f"mode={mode}")
            results.append(entry)
        aggregated = "\n---\n".join(r["response"] for r in results)
        return {"aggregated": aggregated, "results": results}
