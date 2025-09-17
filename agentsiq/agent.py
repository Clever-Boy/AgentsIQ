import time, uuid
from .logger import explain_log
from .governance import check_permission

class Agent:
    def __init__(self, name: str, role: str, model: str = "", allowed_tools=None):
        self.name = name
        self.role = role
        self.model = model or ""  # preferred/base model like 'openai:gpt-4o-mini'
        self.allowed_tools = allowed_tools or []

    def can_use_tool(self, tool_name: str) -> bool:
        return check_permission(self, tool_name)

    def act(self, task: str, router, tools=None):
        """Perform an action for the given task. Uses a tool when appropriate, else routes to an LLM."""
        start = time.time()
        tools = tools or {}
        used_tool = None
        tool_output = None

        # naive heuristic: if task mentions an allowed tool name, use it
        for tname in self.allowed_tools:
            if tname in task.lower() and tname in tools:
                used_tool = tname
                tool_output = tools[tname](task)
                break

        # choose model (either agent's preferred or router's decision)
        model_to_use = None
        if tool_output is None:
            model_to_use = router.select_model(task, preferred=self.model)
            response, confidence = router.call_model(model_to_use, task)
        else:
            response = tool_output
            confidence = 0.9

        latency = time.time() - start
        entry = {
            "agent": self.name,
            "role": self.role,
            "task": task,
            "response": response,
            "model_used": model_to_use if tool_output is None else f"tool:{used_tool}",
            "confidence": confidence,
            "latency": latency,
            "id": str(uuid.uuid4())
        }
        explain_log(entry)
        return entry
