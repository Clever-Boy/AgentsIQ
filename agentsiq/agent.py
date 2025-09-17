import time, uuid
from .logger import explain_log
from .governance import check_permission

class Agent:
    def __init__(self, name: str, role: str, preferred_models=None, allowed_tools=None):
        self.name = name
        self.role = role
        self.preferred_models = preferred_models or []
        self.allowed_tools = allowed_tools or []

    def can_use_tool(self, tool_name):
        return check_permission(self, tool_name)

    def act(self, task: str, router, tools=None):
        """Agent decides how to handle the task: may call router (LLM) or tools.
        Returns a dict with result and metadata for explainability.
        """
        start = time.time()
        # Simple decision: if task mentions a tool the agent is allowed to use, prefer the tool.
        tools = tools or {}
        used_tool = None
        tool_output = None
        for tname in self.allowed_tools:
            if tname in task.lower() and tname in tools:
                used_tool = tname
                tool_output = tools[tname](task)
                break

        # If no tool used, call the router to select a model and get a response
        if tool_output is None:
            model = router.route(task, agent=self)
            response, confidence = router.call_model(model, task)
        else:
            response = tool_output
            confidence = 0.9  # tool outputs assumed confident

        latency = time.time() - start
        entry = {
            "agent": self.name,
            "role": self.role,
            "task": task,
            "response": response,
            "model_used": model if tool_output is None else f"tool:{used_tool}",
            "confidence": confidence,
            "latency": latency,
            "id": str(uuid.uuid4())
        }
        explain_log(entry)
        return entry
