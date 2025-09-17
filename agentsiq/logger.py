import os, json
class Logger:
    def __init__(self, format='json'):
        self.format=format; os.makedirs('logs', exist_ok=True); self.path='logs/decisions.json'
        if not os.path.exists(self.path): open(self.path,'w').write('[]')
    def log_decision(self, agent, decision, model_used, confidence=1.0):
        entry={'agent':agent,'decision':decision,'model':model_used,'confidence':confidence}
        with open(self.path) as f: data=json.load(f)
        data.append(entry)
        with open(self.path,'w') as f: json.dump(data,f,indent=2)
