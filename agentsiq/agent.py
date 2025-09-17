class Agent:
    def __init__(self, name, role, model, allowed_tools=None):
        self.name=name; self.role=role; self.model=model; self.allowed_tools=allowed_tools or []
    def act(self, task):
        return f"[{self.name}] ({self.model}) processed: {task}"
