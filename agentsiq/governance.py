class Governance:
    def __init__(self, policies): self.policies=policies
    def check_permission(self, agent, tool):
        allowed=self.policies.get(agent.name,[])
        return tool in allowed
