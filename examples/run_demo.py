from agentiq.agent import Agent
from agentiq.swarm import Swarm
from agentiq.router import ModelRouter
from agentiq.logger import Logger

def main():
    # Setup agents
    researcher = Agent(name="Researcher", role="Finds information", model="openai:gpt-4o-mini")
    analyst = Agent(name="Analyst", role="Summarizes info", model="anthropic:claude-3-haiku")

    router = ModelRouter(strategy="hybrid")
    logger = Logger(format="json")

    swarm = Swarm(agents=[researcher, analyst], router=router, logger=logger)

    result = swarm.run("Summarize recent advances in multi-agent AI frameworks.")
    print("Final Result:", result)

if __name__ == "__main__":
    main()
