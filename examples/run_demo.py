
from agentsiq.agent import Agent
from agentsiq.collab import Collab
from agentsiq.router import ModelRouter
from agentsiq.obs import init_agentops

init_agentops()

def retrieval(task: str) -> str: 
    return "[retrieval] located 3 relevant sources."

def summarize(task: str) -> str: 
    return "[summary] This is a short summary of the topic."

def main():
    # Create router with hybrid strategy (doesn't rely on Ollama)
    router = ModelRouter()
    router.strategy = "hybrid"  # Use hybrid strategy for reliable model selection
    
    researcher = Agent("Researcher", "Finds information", "openai:gpt-4o-mini", ["retrieval"])
    analyst = Agent("Analyst", "Summarizes info", "anthropic:claude-3-haiku", ["summarize"])
    
    collab = Collab([researcher, analyst], {"retrieval": retrieval, "summarize": summarize})
    
    task = "Summarize recent advances in multi-agent AI frameworks and give a tiny python code example."
    
    print(f"🎯 Task: {task}")
    print(f"⚙️ Router Strategy: {router.strategy}")
    print("🚀 Running collaboration...")
    
    out = collab.run(task)
    
    print("\nAGGREGATED OUTPUT")
    print("==================")
    print(out["aggregated"])
    
    print("\n📊 Individual Results:")
    for i, result in enumerate(out["results"], 1):
        print(f"\n{i}. {result['agent']}:")
        print(f"   Model: {result['model_used']}")
        print(f"   Response: {result['response'][:100]}...")
    
    print("\n💡 Next Steps:")
    print("   Start: python -m examples.serve_and_demo  -> single process with shared router + UI control")

if __name__ == "__main__": 
    main()
