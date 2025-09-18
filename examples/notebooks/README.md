# 📓 AgentsIQ Jupyter Notebook Examples

This directory contains comprehensive Jupyter notebook examples demonstrating how to build intelligent agents using AgentsIQ's multi-model routing system.

## 🎯 Available Notebooks

### 1. **Basic Search Agent** (`search_agent_basic.ipynb`)
**Perfect for beginners** - Learn the fundamentals of creating search agents with AgentsIQ.

**Features:**
- Simple search agent setup
- Basic model routing
- Cost optimization
- Performance monitoring
- Interactive search interface

**What you'll learn:**
- How to initialize AgentsIQ router
- Creating agents with specific capabilities
- Implementing search tools
- Analyzing model selection decisions
- Building interactive interfaces

### 2. **Advanced Search Agent** (`search_agent_advanced.ipynb`)
**For intermediate users** - Build sophisticated search systems with multi-agent collaboration.

**Features:**
- Multi-agent collaboration
- Real web search integration
- Advanced result processing
- Specialized agent types
- Complex query handling

**What you'll learn:**
- Multi-agent system design
- Web scraping and data extraction
- Result ranking and filtering
- Agent specialization
- Advanced analytics

### 3. **Research Agent** (`research_agent.ipynb`)
**For research professionals** - Create agents specialized in comprehensive research tasks.

**Features:**
- Deep research capabilities
- Multi-source analysis
- Report generation
- Fact-checking
- Citation management

**What you'll learn:**
- Research workflow automation
- Source credibility assessment
- Report structuring
- Data synthesis
- Quality assurance

### 4. **Complete Agent System** (`complete_agent_system.ipynb`)
**For advanced users** - Build enterprise-grade multi-agent systems.

**Features:**
- Full multi-agent ecosystem
- Task orchestration
- System monitoring
- Performance optimization
- Scalable architecture

**What you'll learn:**
- System architecture design
- Agent coordination
- Load balancing
- Monitoring and alerting
- Production deployment

## 🚀 Quick Start

### Prerequisites
```bash
# Install AgentsIQ
pip install agentsiq

# Install additional dependencies for notebooks
pip install jupyter requests beautifulsoup4 matplotlib pandas
```

### Running the Notebooks
```bash
# Start Jupyter Lab
jupyter lab

# Or start Jupyter Notebook
jupyter notebook
```

### Environment Setup
Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
GROK_API_KEY=your_grok_key_here
OLLAMA_URL=http://localhost:11434
AGENTOPS_API_KEY=your_agentops_key_here
```

## 📚 Learning Path

### **Beginner Path:**
1. Start with `search_agent_basic.ipynb`
2. Understand model routing concepts
3. Experiment with different search queries
4. Analyze performance metrics

### **Intermediate Path:**
1. Complete the basic search agent
2. Move to `search_agent_advanced.ipynb`
3. Learn multi-agent collaboration
4. Implement real web search

### **Advanced Path:**
1. Master the advanced search agent
2. Explore `research_agent.ipynb`
3. Build specialized research workflows
4. Implement `complete_agent_system.ipynb`

### **Expert Path:**
1. Customize all agent types
2. Build your own specialized agents
3. Integrate with external systems
4. Deploy production systems

## 🛠️ Customization Guide

### **Creating Custom Agents**
```python
from agentsiq.agent import Agent

# Define your custom agent
custom_agent = Agent(
    name="MyAgent",
    description="Custom agent for specific tasks",
    preferred_model="openai:gpt-4o-mini",
    tools=["custom_tool1", "custom_tool2"]
)
```

### **Implementing Custom Tools**
```python
def custom_tool(input_data: str) -> str:
    """Your custom tool implementation"""
    # Process input_data
    result = process_data(input_data)
    return result

# Add to tools dictionary
tools = {
    "custom_tool": custom_tool,
    # ... other tools
}
```

### **Configuring Model Routing**
```python
from agentsiq.router import ModelRouter

# Create router with custom weights
router = ModelRouter()
router.set_weights(cost=0.7, latency=0.2, quality=0.1)

# Or use different strategy
router.set_strategy("hybrid")
```

## 📊 Performance Monitoring

### **Real-time Analytics**
```python
from agentsiq.decision_store import latest_decisions

# Get recent decisions
decisions = latest_decisions(100)

# Analyze performance
for decision in decisions:
    print(f"Model: {decision['chosen']}")
    print(f"Cost: ${decision.get('est_cost_chosen', 0):.6f}")
    print(f"Savings: ${decision.get('est_cost_saved_vs_gpt4o', 0):.6f}")
```

### **Dashboard Integration**
```python
# Start the dashboard
from agentsiq.dashboard import app
import uvicorn

uvicorn.run(app, host="127.0.0.1", port=8000)
# Visit http://127.0.0.1:8000 for real-time monitoring
```

## 🔧 Troubleshooting

### **Common Issues:**

1. **Import Errors**
   ```bash
   pip install --upgrade agentsiq
   ```

2. **API Key Issues**
   - Check your `.env` file
   - Verify API key validity
   - Ensure proper environment variable loading

3. **Model Selection Issues**
   - Check model availability
   - Verify configuration in `config.yaml`
   - Review routing strategy settings

4. **Performance Issues**
   - Monitor model costs and latency
   - Adjust routing weights
   - Consider using local models (Ollama)

### **Getting Help:**
- Check the [Architecture Documentation](../docs/architecture.md)
- Review [PyPI Distribution Guide](../docs/pypi_distribution.md)
- Open an issue on GitHub
- Join our community discussions

## 🎉 Next Steps

After completing these notebooks, you'll be ready to:

1. **Build Production Systems** - Deploy agents in real-world applications
2. **Customize for Your Domain** - Adapt agents for specific industries
3. **Scale Your System** - Handle high-volume agent operations
4. **Integrate with External Systems** - Connect with databases, APIs, and services
5. **Monitor and Optimize** - Continuously improve agent performance

## 📈 Success Metrics

Track your progress with these key metrics:

- **Cost Efficiency**: Monitor savings vs baseline models
- **Response Quality**: Measure answer accuracy and relevance
- **System Performance**: Track latency and throughput
- **User Satisfaction**: Gather feedback on agent responses
- **Model Utilization**: Analyze which models are used most

Happy building with AgentsIQ! 🚀

