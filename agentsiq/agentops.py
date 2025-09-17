import os, csv, time, json
RECORD_DIR = os.path.join(os.path.dirname(__file__), '..', 'agentops_records')
os.makedirs(RECORD_DIR, exist_ok=True)
CSV_FILE = os.path.join(RECORD_DIR, 'agentops_metrics.csv')

# Ensure header
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['timestamp','agent','task_id','model_used','confidence','latency','note'])

def record_metrics(entry: dict, note: str = ''):
    """Record metrics to CSV and mirror JSON per-run. Entry should contain agent, id, model_used, confidence, latency."""
    ts = time.time()
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow([ts, entry.get('agent'), entry.get('id'), entry.get('model_used'), entry.get('confidence'), entry.get('latency'), note])
    # also write a JSON dump for the run
    fname = os.path.join(RECORD_DIR, f"run_{entry.get('id')}.json")
    with open(fname, 'w', encoding='utf-8') as jf:
        json.dump(entry, jf, ensure_ascii=False, indent=2)
