import os, json, time
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, f"explain_log_{int(time.time())}.jsonl")

def explain_log(entry: dict):
    """Append a JSON line with the decision trace. Entry should include agent, role, task, response, model_used, confidence, latency."""
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')
