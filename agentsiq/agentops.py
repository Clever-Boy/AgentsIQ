import os,json
class AgentOps:
    def __init__(self): os.makedirs('agentops_records',exist_ok=True); self.path='agentops_records/metrics.json';
        if not os.path.exists(self.path): open(self.path,'w').write('{}')
    def record(self, metric, value):
        with open(self.path) as f: data=json.load(f)
        data[metric]=value
        with open(self.path,'w') as f: json.dump(data,f,indent=2)
