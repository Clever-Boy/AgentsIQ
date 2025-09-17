
import os,csv,json,time
REC_DIR=os.path.join(os.getcwd(),"agentops_records"); os.makedirs(REC_DIR,exist_ok=True)
CSV_PATH=os.path.join(REC_DIR,"metrics.csv")
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["ts","agent","task_id","model","confidence","latency","note"])
def record(entry:dict,note:str=""):
    ts=time.time()
    with open(CSV_PATH,"a",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow([ts,entry.get("agent"),entry.get("id"),entry.get("model_used"),entry.get("confidence"),entry.get("latency"),note])
    with open(os.path.join(REC_DIR,f"run_{entry.get('id')}.json"),"w",encoding="utf-8") as jf:
        json.dump(entry,jf,ensure_ascii=False,indent=2)
def summary_by_agent():
    if not os.path.exists(CSV_PATH): return {}
    rows=[]
    with open(CSV_PATH,"r",encoding="utf-8") as f:
        r=csv.DictReader(f)
        for row in r:
            row["latency"]=float(row.get("latency") or 0.0); row["confidence"]=float(row.get("confidence") or 0.0)
            rows.append(row)
    by={}
    for row in rows:
        ag=row["agent"]; by.setdefault(ag,{"calls":0,"avg_latency":0,"avg_confidence":0,"models":{}})
        d=by[ag]; d["calls"]+=1; d["avg_latency"]+=row["latency"]; d["avg_confidence"]+=row["confidence"]
        mdl=row["model"]; d["models"][mdl]=d["models"].get(mdl,0)+1
    for d in by.values():
        if d["calls"]:
            d["avg_latency"]/=d["calls"]; d["avg_confidence"]/=d["calls"]
    return by
