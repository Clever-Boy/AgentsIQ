from agentsiq.agent import Agent
from agentsiq.swarm import Swarm
from agentsiq.router import ModelRouter

# simple tools
def retrieval(task: str) -> str:
    return "[retrieval] located 3 relevant sources."

def summarize(task: str) -> str:
    return "[summary] This is a short summary of the topic."

def main():
    researcher = Agent(name="Researcher", role="Finds information", model="openai:gpt-4o-mini", allowed_tools=["retrieval"])
    analyst = Agent(name="Analyst", role="Summarizes info", model="anthropic:claude-3-haiku", allowed_tools=["summarize"])

    router = ModelRouter(strategy="hybrid")
    swarm = Swarm(agents=[researcher, analyst], router=router, tools={"retrieval": retrieval, "summarize": summarize})

    out = swarm.run("Summarize recent advances in multi-agent AI frameworks, and provide a short python code example.")
    print("\nAGGREGATED OUTPUT\n==================\n", out["aggregated"])
    print("\nSee logs/ and agentops_records/ for traces and metrics.")

if __name__ == "__main__":
    main()
