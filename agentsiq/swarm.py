from typing import List
from .router import ModelRouter
from .agent import Agent
from .agentops import record_metrics

class Swarm:
    def __init__(self, agents: List[Agent], router: ModelRouter = None, tools: dict = None):
        self.agents = agents
        self.router = router or ModelRouter()
        self.tools = tools or {}

    def run(self, task: str, mode: str = 'sequential'):
        """Simple orchestration: sequentially ask agents to act and aggregate results.
        mode: 'sequential' or 'parallel' (parallel simulated sequentially here for MVP)
        Returns list of agent entries.
        """
        results = []
        for agent in self.agents:
            entry = agent.act(task, router=self.router, tools=self.tools)
            # record to AgentOps
            record_metrics(entry, note=f"swarm_mode:{mode}")
            results.append(entry)
        # Simple aggregation: return combined responses
        agg = '\n---\n'.join([r['response'] for r in results])
        return {'aggregated': agg, 'results': results}
