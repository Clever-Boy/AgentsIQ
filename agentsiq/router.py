class ModelRouter:
    def __init__(self, strategy='hybrid'):
        self.strategy=strategy
    def select_model(self, task):
        if self.strategy=='cheapest':
            return 'anthropic:claude-3-haiku'
        elif self.strategy=='fastest':
            return 'google:gemini-pro'
        else:
            return 'openai:gpt-4o-mini'
