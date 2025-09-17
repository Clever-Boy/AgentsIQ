
from agentsiq.agent import Agent
from agentsiq.swarm import Swarm
from agentsiq.router import ModelRouter

def retrieval(task: str) -> str: return "[retrieval] located 3 relevant sources."
def summarize(task: str) -> str: return "[summary] This is a short summary of the topic."

def main():
    researcher=Agent("Researcher","Finds information","openai:gpt-4o-mini",["retrieval"])
    analyst=Agent("Analyst","Summarizes info","anthropic:claude-3-haiku",["summarize"])
    router=ModelRouter(strategy="smart")
    swarm=Swarm([researcher,analyst],router,{"retrieval":retrieval,"summarize":summarize})
    task="Summarize recent advances in multi-agent AI frameworks and give a tiny python code example."
    out=swarm.run(task)
    print("\nAGGREGATED OUTPUT\n==================\n", out["aggregated"])
    print("\nOpen http://127.0.0.1:8000/decisions to see WHY a model was chosen.")
if __name__=="__main__": main()
