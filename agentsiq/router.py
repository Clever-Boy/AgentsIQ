import time, random, os

class LLMClientMock:
    """A mock LLM client that simulates responses. Replace with real provider calls."""
    def __init__(self, name):
        self.name = name

    def generate(self, prompt: str):
        # deterministic-ish mock response
        time.sleep(0.2)
        return f"[{self.name} MOCK RESPONSE] {prompt[:200]}", random.uniform(0.6, 0.95)

class ModelRouter:
    def __init__(self, heuristics=None):
        # heuristics: a dict of lists to detect keywords
        self.heuristics = heuristics or {}
        # instantiate mock clients for configured model names (lazy)
        self.clients = {}

    def _get_client(self, model_name):
        if model_name not in self.clients:
            self.clients[model_name] = LLMClientMock(model_name)
        return self.clients[model_name]

    def route(self, task: str, agent=None):
        """Decide which model to use based on simple heuristics and agent preferences."""
        t = task.lower()
        # If agent has preferred models, try them in order if matching heuristics
        if agent and getattr(agent, 'preferred_models', None):
            # quick heuristic: if task mentions 'code' choose first preferred that looks like code model
            if 'code' in t or 'implement' in t:
                for m in agent.preferred_models:
                    if 'gpt' in m or 'code' in m:
                        return m
            # if task asks to summarize pick a cheaper/smaller model from preferences
            if any(k in t for k in self.heuristics.get('summarize_keywords', [])):
                for m in agent.preferred_models:
                    if 'claude' in m or 'gemini' in m:
                        return m
            # fallback to first preferred
            return agent.preferred_models[0]

        # global heuristics
        if any(k in t for k in self.heuristics.get('code_keywords', [])):
            return 'gpt-4'
        if any(k in t for k in self.heuristics.get('summarize_keywords', [])):
            return 'claude-2'
        # default
        return 'gpt-4'

    def call_model(self, model_name: str, prompt: str):
        client = self._get_client(model_name)
        return client.generate(prompt)
