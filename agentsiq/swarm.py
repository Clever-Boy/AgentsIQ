class Swarm:
    def __init__(self, agents, router, logger):
        self.agents=agents; self.router=router; self.logger=logger
    def run(self, task):
        chosen=self.router.select_model(task)
        self.logger.log_decision(agent='Swarm', decision='Routed', model_used=chosen)
        results=[a.act(task) for a in self.agents]
        self.logger.log_decision(agent='Swarm', decision='Completed', model_used=chosen)
        return results[-1]
