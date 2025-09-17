# Demo for AgentIQ minimal MVP
from agentiq.agent import Agent
from agentiq.swarm import Swarm
from agentiq.router import ModelRouter
from agentiq.agentops import RECORD_DIR

# Example simple tools
def retrieval_tool(task):
    return "[retrieval] Found 3 documents related to: " + task[:120]

def summarize_tool(task):
    return "[summarize] Short summary: " + (task[:140] + '...')

def main():
    heuristics = {
        'code_keywords': ['code', 'implement', 'algorithm', 'python'],
        'summarize_keywords': ['summarize', 'summary', 'tl;dr', 'short']
    }
    router = ModelRouter(heuristics=heuristics)

    researcher = Agent(name='Researcher', role='researcher', preferred_models=['gpt-4','gpt-4o'], allowed_tools=['retrieval'])
    analyst = Agent(name='Analyst', role='analyst', preferred_models=['claude-2','gemini-pro'], allowed_tools=['summarize'])

    swarm = Swarm(agents=[researcher, analyst], router=router, tools={
        'retrieval': retrieval_tool,
        'summarize': summarize_tool
    })

    task = "Summarize recent advances in multi-agent AI frameworks and implement a simple python example code."
    output = swarm.run(task)
    print("\nAGGREGATED OUTPUT:\n", output['aggregated'])
    print("\nAgentOps records stored in:", RECORD_DIR)

if __name__ == '__main__':
    main()
