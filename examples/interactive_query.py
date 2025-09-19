#!/usr/bin/env python3
"""
Interactive Query Tool for AgentsIQ
==================================

This tool allows users to enter queries and see how AgentsIQ intelligently selects models
based on task traits, cost, latency, and quality. Users can choose different routing strategies
and see detailed explanations of the decision-making process.

Usage:
    python examples/interactive_query.py
"""

import sys
import os
import time
from datetime import datetime

# Add src to path and ensure it's first to use local source code
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Force reload of agentsiq modules to use local source code
import importlib
if 'agentsiq' in sys.modules:
    importlib.reload(sys.modules['agentsiq'])
    if 'agentsiq.router' in sys.modules:
        importlib.reload(sys.modules['agentsiq.router'])
    if 'agentsiq.config_loader' in sys.modules:
        importlib.reload(sys.modules['agentsiq.config_loader'])

from agentsiq.router import ModelRouter
from agentsiq.agent import Agent
from agentsiq.collab import Collab
from agentsiq.decision_store import latest_decisions

def print_banner():
    """Print a welcome banner"""
    print("=" * 80)
    print("🚀 AgentsIQ Interactive Query Tool")
    print("=" * 80)
    print("Enter queries to see intelligent model selection in action!")
    print("Type 'help' for commands, 'quit' to exit")
    print("=" * 80)

def print_help():
    """Print help information"""
    print("\n📖 Available Commands:")
    print("  help          - Show this help message")
    print("  strategies    - Show available routing strategies")
    print("  models        - Show available models and their profiles")
    print("  history       - Show recent model selection decisions")
    print("  dashboard     - Show performance dashboard")
    print("  select        - Interactive model selection")
    print("  debug         - Show debug information for availability checking")
    print("  clear         - Clear screen")
    print("  quit/exit     - Exit the program")
    print("\n💡 Just type your query to see intelligent model selection!")

def print_strategies():
    """Print available routing strategies"""
    print("\n⚙️ Available Routing Strategies:")
    print("  smart         - Multi-objective optimization (cost, latency, quality)")
    print("  hybrid        - Task-specific model selection (code→GPT-4o, summary→Claude)")
    print("  cheapest      - Always choose the lowest cost model")
    print("  fastest       - Always choose the fastest model")
    print("\n💡 Use 'strategy <name>' to change strategy")

def print_models(router):
    """Print available models and their profiles"""
    print("\n🤖 Available Models:")
    print("-" * 100)
    print(f"{'#':<3} {'Model':<25} {'Provider':<12} {'Cost':<8} {'Latency':<8} {'Quality':<8} {'Summary':<30}")
    print("-" * 100)
    
    model_summaries = {
        "openai:gpt-4o-mini": "Fast, cost-effective, good for most tasks",
        "openai:gpt-4o": "Most capable, best for complex coding and analysis",
        "anthropic:claude-3-haiku": "Excellent for summaries and general tasks",
        "google:gemini-pro": "Good general purpose, fast responses",
        "ollama:llama3.1:8b": "Local, free, good for basic tasks",
        "ollama:llama3.1:70b": "Local, free, high quality but slower",
        "ollama:qwen2.5:7b": "Local, free, very fast responses",
        "ollama:qwen2.5:72b": "Local, free, high quality, moderate speed",
        "grok:grok-2": "X.AI model, good for general tasks",
        "grok:grok-2-vision": "X.AI model with vision capabilities"
    }
    
    for i, (model, profile) in enumerate(router.profiles.items(), 1):
        provider = model.split(':')[0].title()
        cost = f"${profile['cost']:.3f}"
        latency = f"{profile['latency']:.2f}s"
        quality = f"{profile['quality']:.2f}"
        summary = model_summaries.get(model, "General purpose model")
        
        print(f"{i:<3} {model:<25} {provider:<12} {cost:<8} {latency:<8} {quality:<8} {summary:<30}")
    
    print("-" * 100)

def analyze_query(router, query):
    """Analyze a query and show trait detection"""
    from agentsiq.router import _traits, _estimate_tokens
    
    tokens = _estimate_tokens(query)
    traits = _traits(query)
    
    print(f"\n🔍 Query Analysis:")
    print(f"  Query: {query}")
    print(f"  Estimated Tokens: {tokens}")
    print(f"  Detected Traits:")
    
    trait_descriptions = {
        "is_code": "Contains code or programming concepts",
        "is_summary": "Asks for summarization or TL;DR",
        "has_math": "Contains mathematical expressions or calculations",
        "is_creative": "Requires creative writing or generation",
        "is_analytical": "Requires analysis or reasoning",
        "is_factual": "Asks for factual information"
    }
    
    for trait, description in trait_descriptions.items():
        status = "✅" if traits.get(trait, False) else "❌"
        print(f"    {status} {trait}: {description}")

def show_model_recommendations(router, query):
    """Show model recommendations for different strategies"""
    from agentsiq.router import _traits, _estimate_tokens
    
    tokens = _estimate_tokens(query)
    traits = _traits(query)
    
    print(f"\n🎯 Model Recommendations:")
    print("-" * 60)
    
    # Test different strategies
    strategies = ["smart", "hybrid", "cheapest", "fastest"]
    
    for strategy in strategies:
        original_strategy = router.strategy
        router.strategy = strategy
        
        if strategy == "cheapest":
            chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["cost"])
        elif strategy == "fastest":
            chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["latency"])
        elif strategy == "hybrid":
            if traits["is_code"]:
                chosen = "openai:gpt-4o"
            elif traits["is_summary"]:
                chosen = "anthropic:claude-3-haiku"
            else:
                chosen = "openai:gpt-4o-mini"
        else:  # smart - simulate smart selection
            # Calculate efficiency for smart strategy
            best_model = None
            best_efficiency = -1
            
            for model in router.profiles.keys():
                profile = router.profiles[model]
                tokens_out = min(1500, int(tokens * 2.0))
                tokens_total = tokens + tokens_out
                est_cost = profile["cost"] * (tokens_total / 1000.0)
                quality = profile.get("quality", 0.75)
                
                # Apply trait-based quality boosts
                if traits["is_code"] and "openai" in model:
                    quality += 0.05
                if traits["is_summary"] and "anthropic" in model:
                    quality += 0.05
                if "gemini" in model and not traits["is_code"]:
                    quality += 0.02
                
                quality = max(0.6, min(0.98, quality))
                efficiency = quality / max(est_cost, 0.001)
                
                if efficiency > best_efficiency:
                    best_efficiency = efficiency
                    best_model = model
            
            chosen = best_model or "openai:gpt-4o-mini"
        
        profile = router.profiles[chosen]
        print(f"  {strategy.upper():<8}: {chosen}")
        print(f"           Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f}")
        
        router.strategy = original_strategy

def show_smart_analysis(router, query):
    """Show detailed smart strategy analysis"""
    from agentsiq.router import _traits, _estimate_tokens
    
    tokens = _estimate_tokens(query)
    traits = _traits(query)
    
    print(f"\n🧠 Smart Strategy Analysis:")
    print("-" * 60)
    
    # Simulate smart scoring by calculating cost-efficiency
    scored = []
    for model in router.profiles.keys():
        profile = router.profiles[model]
        tokens_out = min(1500, int(tokens * 2.0))
        tokens_total = tokens + tokens_out
        est_cost = profile["cost"] * (tokens_total / 1000.0)
        quality = profile.get("quality", 0.75)
        
        # Apply trait-based quality boosts
        if traits["is_code"] and "openai" in model:
            quality += 0.05
        if traits["is_summary"] and "anthropic" in model:
            quality += 0.05
        if "gemini" in model and not traits["is_code"]:
            quality += 0.02
        
        quality = max(0.6, min(0.98, quality))
        
        # Calculate efficiency score (quality per cost)
        efficiency = quality / max(est_cost, 0.001)
        scored.append((model, efficiency, est_cost, quality))
    
    scored.sort(key=lambda x: x[1], reverse=True)  # Higher efficiency is better
    
    print(f"{'Rank':<4} {'Model':<25} {'Efficiency':<10} {'Cost':<8} {'Latency':<8} {'Quality':<8}")
    print("-" * 80)
    
    for i, (model, efficiency, est_cost, quality) in enumerate(scored, 1):  # Show all models
        profile = router.profiles[model]
        print(f"{i:<4} {model:<25} {efficiency:.2f}     ${est_cost:.4f}   {profile['latency']:.2f}s     {quality:.2f}")

def show_history():
    """Show recent model selection decisions"""
    decisions = latest_decisions(10)
    
    if not decisions:
        print("\n📊 No decision history available yet.")
        return
    
    print(f"\n📊 Recent Model Selection Decisions:")
    print("-" * 80)
    
    for i, decision in enumerate(decisions, 1):
        print(f"\n{i}. Task: {decision.get('task', 'N/A')[:50]}...")
        print(f"   Model: {decision.get('chosen', 'N/A')}")
        print(f"   Strategy: {decision.get('strategy', 'N/A')}")
        print(f"   Cost: ${decision.get('est_cost_chosen', 0):.4f}")
        print(f"   Latency: {decision.get('latency', 0):.2f}s")
        print(f"   Quality: {decision.get('quality', 0):.2f}")

def show_dashboard():
    """Show a simple performance dashboard"""
    decisions = latest_decisions(50)
    
    if not decisions:
        print("\n📊 No data available for dashboard yet.")
        return
    
    print(f"\n📊 Performance Dashboard:")
    print("-" * 60)
    
    # Model usage count
    model_counts = {}
    total_cost = 0
    total_latency = 0
    total_quality = 0
    
    for decision in decisions:
        model = decision.get('chosen', 'unknown')
        model_counts[model] = model_counts.get(model, 0) + 1
        total_cost += decision.get('est_cost_chosen', 0)
        total_latency += decision.get('latency', 0)
        total_quality += decision.get('quality', 0)
    
    print(f"Total Decisions: {len(decisions)}")
    print(f"Total Cost: ${total_cost:.4f}")
    print(f"Average Latency: {total_latency/len(decisions):.2f}s")
    print(f"Average Quality: {total_quality/len(decisions):.3f}")
    
    print(f"\nModel Usage:")
    for model, count in sorted(model_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(decisions)) * 100
        print(f"  {model}: {count} times ({percentage:.1f}%)")

def interactive_model_selection(router, query):
    """Interactive model selection for a specific query"""
    from agentsiq.router import _traits, _estimate_tokens
    
    traits = _traits(query)
    tokens = _estimate_tokens(query)
    
    print(f"\n🎯 Interactive Model Selection for:")
    print(f"Query: {query}")
    print(f"Traits: {', '.join([k for k, v in traits.items() if v])}")
    print("-" * 60)
    
    # Show all models with numbers
    print_models(router)
    
    # Get recommendations based on current strategy
    print(f"\n💡 Recommendations for '{router.strategy}' strategy:")
    if router.strategy == "smart":
        # Calculate efficiency scores
        scored = []
        for model in router.profiles.keys():
            profile = router.profiles[model]
            tokens_out = min(1500, int(tokens * 2.0))
            tokens_total = tokens + tokens_out
            est_cost = profile["cost"] * (tokens_total / 1000.0)
            quality = profile.get("quality", 0.75)
            
            # Apply trait-based quality boosts
            if traits["is_code"] and "openai" in model:
                quality += 0.05
            if traits["is_summary"] and "anthropic" in model:
                quality += 0.05
            if "gemini" in model and not traits["is_code"]:
                quality += 0.02
            
            quality = max(0.6, min(0.98, quality))
            efficiency = quality / max(est_cost, 0.001)
            
            scored.append((model, efficiency, est_cost, quality))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        
        print("Top 3 recommended models:")
        for i, (model, efficiency, est_cost, quality) in enumerate(scored[:3], 1):
            profile = router.profiles[model]
            print(f"  {i}. {model} (Efficiency: {efficiency:.2f}, Cost: ${est_cost:.4f})")
    
    elif router.strategy == "hybrid":
        if traits["is_code"]:
            chosen = "openai:gpt-4o"
        elif traits["is_summary"]:
            chosen = "anthropic:claude-3-haiku"
        else:
            chosen = "openai:gpt-4o-mini"
        print(f"Recommended: {chosen}")
    
    elif router.strategy == "cheapest":
        chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["cost"])
        print(f"Recommended: {chosen}")
    
    elif router.strategy == "fastest":
        chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["latency"])
        print(f"Recommended: {chosen}")
    
    # Let user select
    while True:
        try:
            choice = input(f"\nSelect model (1-{len(router.profiles)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(router.profiles):
                selected_model = list(router.profiles.keys())[choice_idx]
                profile = router.profiles[selected_model]
                
                print(f"\n✅ Selected: {selected_model}")
                print(f"   Cost: ${profile['cost']:.3f} per 1K tokens")
                print(f"   Latency: {profile['latency']:.2f} seconds")
                print(f"   Quality: {profile['quality']:.2f}")
                
                return selected_model
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a number or 'q' to quit.")
        except KeyboardInterrupt:
            return None

def check_model_availability(router, model):
    """Check if a model is available"""
    # Load environment variables from .env file
    from dotenv import load_dotenv
    load_dotenv()
    
    if model.startswith("ollama:"):
        try:
            import requests
            ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
            response = requests.get(f"{ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                # Check if the specific model is actually available
                models = response.json().get("models", [])
                model_name = model.split(":", 1)[1]
                return any(m.get("name", "").startswith(model_name) for m in models)
            return False
        except:
            return False
    elif model.startswith("openai:"):
        api_key = os.getenv("OPENAI_API_KEY")
        return api_key is not None and len(api_key.strip()) > 0 and not api_key.startswith("your_")
    elif model.startswith("anthropic:"):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        return api_key is not None and len(api_key.strip()) > 0 and not api_key.startswith("your_")
    elif model.startswith("google:"):
        api_key = os.getenv("GOOGLE_API_KEY")
        return api_key is not None and len(api_key.strip()) > 0 and not api_key.startswith("your_") and api_key.startswith("AIzaSy")
    elif model.startswith("grok:"):
        api_key = os.getenv("GROK_API_KEY")
        return api_key is not None and len(api_key.strip()) > 0 and not api_key.startswith("your_")
    return True  # Assume available if we can't check

def process_query(router, query):
    """Process a query and show the intelligent routing"""
    print(f"\n🚀 Processing Query: {query}")
    print("=" * 60)
    
    # Analyze the query
    analyze_query(router, query)
    
    # Show model recommendations
    show_model_recommendations(router, query)
    
    # Show smart analysis if using smart strategy
    if router.strategy == "smart":
        show_smart_analysis(router, query)
    
    # Ask user to select from all models
    print(f"\n🎯 Select Model for Processing:")
    print("-" * 50)
    
    # Get all models instead of just recommendations
    all_models = list(router.profiles.keys())
    
    # Check availability and show options
    available_options = []
    unavailable_options = []
    
    for i, model in enumerate(all_models, 1):
        is_available = check_model_availability(router, model)
        profile = router.profiles[model]
        
        if is_available:
            available_options.append((i, model, profile))
            print(f"{i}. ✅ {model} (Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f})")
        else:
            unavailable_options.append((i, model, profile))
            print(f"{i}. ❌ {model} (NOT AVAILABLE - Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f})")
    
    # Let user select
    while True:
        try:
            choice = input(f"\nSelect model (1-{len(all_models)}) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                return "quit"
            
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(all_models):
                selected_model = all_models[choice_idx]
                is_available = check_model_availability(router, selected_model)
                
                if not is_available:
                    print(f"❌ {selected_model} is not available. Please select another model.")
                    continue
                
                print(f"\n✅ Selected: {selected_model}")
                break
            else:
                print("❌ Invalid choice. Please try again.")
                
        except ValueError:
            print("❌ Please enter a number or 'q' to quit.")
        except KeyboardInterrupt:
            return
    
    # Process the query with selected model
    print(f"\n⚡ Processing with {selected_model}...")
    
    # Call the model directly to ensure we use the selected model
    start_time = time.time()
    response, confidence = router.call_model(selected_model, query)
    end_time = time.time()
    
    print(f"\n✅ Query Processed!")
    print(f"   Model Used: {selected_model}")
    print(f"   Processing Time: {end_time - start_time:.2f}s")
    print(f"   Confidence: {confidence:.2f}")
    print(f"   Response: {response}")
    
    if len(response) > 200:
        print("   ... (truncated)")

def get_strategy_recommendations(router, query):
    """Get model recommendations based on current strategy"""
    from agentsiq.router import _traits, _estimate_tokens
    
    traits = _traits(query)
    tokens = _estimate_tokens(query)
    
    if router.strategy == "smart":
        # Calculate efficiency scores
        scored = []
        for model in router.profiles.keys():
            profile = router.profiles[model]
            tokens_out = min(1500, int(tokens * 2.0))
            tokens_total = tokens + tokens_out
            est_cost = profile["cost"] * (tokens_total / 1000.0)
            quality = profile.get("quality", 0.75)
            
            # Apply trait-based quality boosts
            if traits["is_code"] and "openai" in model:
                quality += 0.05
            if traits["is_summary"] and "anthropic" in model:
                quality += 0.05
            if "gemini" in model and not traits["is_code"]:
                quality += 0.02
            
            quality = max(0.6, min(0.98, quality))
            efficiency = quality / max(est_cost, 0.001)
            
            scored.append((model, efficiency))
        
        scored.sort(key=lambda x: x[1], reverse=True)
        return [model for model, _ in scored[:5]]  # Top 5
    
    elif router.strategy == "hybrid":
        if traits["is_code"]:
            return ["openai:gpt-4o", "openai:gpt-4o-mini", "anthropic:claude-3-haiku"]
        elif traits["is_summary"]:
            return ["anthropic:claude-3-haiku", "openai:gpt-4o-mini", "google:gemini-pro"]
        else:
            return ["openai:gpt-4o-mini", "google:gemini-pro", "anthropic:claude-3-haiku"]
    
    elif router.strategy == "cheapest":
        cheapest_models = sorted(router.profiles.keys(), key=lambda m: router.profiles[m]["cost"])
        return cheapest_models[:5]
    
    elif router.strategy == "fastest":
        fastest_models = sorted(router.profiles.keys(), key=lambda m: router.profiles[m]["latency"])
        return fastest_models[:5]
    
    return list(router.profiles.keys())[:5]

def show_all_available_models(router):
    """Show all models with availability status"""
    print(f"\n🤖 All Models with Availability Status:")
    print("-" * 100)
    print(f"{'#':<3} {'Model':<25} {'Status':<12} {'Cost':<8} {'Latency':<8} {'Quality':<8} {'Summary':<30}")
    print("-" * 100)
    
    model_summaries = {
        "openai:gpt-4o-mini": "Fast, cost-effective, good for most tasks",
        "openai:gpt-4o": "Most capable, best for complex coding and analysis",
        "anthropic:claude-3-haiku": "Excellent for summaries and general tasks",
        "google:gemini-pro": "Good general purpose, fast responses",
        "ollama:llama3.1:8b": "Local, free, good for basic tasks",
        "ollama:llama3.1:70b": "Local, free, high quality but slower",
        "ollama:qwen2.5:7b": "Local, free, very fast responses",
        "ollama:qwen2.5:72b": "Local, free, high quality, moderate speed",
        "grok:grok-2": "X.AI model, good for general tasks",
        "grok:grok-2-vision": "X.AI model with vision capabilities"
    }
    
    for i, (model, profile) in enumerate(router.profiles.items(), 1):
        is_available = check_model_availability(router, model)
        status = "✅ Available" if is_available else "❌ Not Available"
        cost = f"${profile['cost']:.3f}"
        latency = f"{profile['latency']:.2f}s"
        quality = f"{profile['quality']:.2f}"
        summary = model_summaries.get(model, "General purpose model")
        
        print(f"{i:<3} {model:<25} {status:<12} {cost:<8} {latency:<8} {quality:<8} {summary:<30}")
    
    print("-" * 100)

def show_debug_info():
    """Show debug information for availability checking"""
    from dotenv import load_dotenv
    load_dotenv()
    
    print(f"\n🔍 Debug Information:")
    print("-" * 60)
    
    # Check .env file loading
    print("📁 Environment Variables:")
    api_keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "GROK_API_KEY": os.getenv("GROK_API_KEY"),
        "OLLAMA_URL": os.getenv("OLLAMA_URL", "http://localhost:11434")
    }
    
    for key, value in api_keys.items():
        if value:
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"  {key}: {masked_value}")
        else:
            print(f"  {key}: Not set")
    
    # Check Ollama specifically
    print(f"\n🦙 Ollama Status:")
    try:
        import requests
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"  ✅ Ollama server is running at {ollama_url}")
            print(f"  📋 Available models: {[m.get('name', 'unknown') for m in models]}")
        else:
            print(f"  ❌ Ollama server returned status {response.status_code}")
    except Exception as e:
        print(f"  ❌ Ollama server is not accessible: {e}")
    
    # Check .env file location
    print(f"\n📄 .env File Status:")
    env_files = [".env", "config/.env", "../.env", "../../.env"]
    for env_file in env_files:
        if os.path.exists(env_file):
            print(f"  ✅ Found .env file at: {env_file}")
            break
    else:
        print(f"  ❌ No .env file found in common locations")
        print(f"  💡 Make sure your .env file is in the project root or config/ directory")
    
    print("-" * 60)

def main():
    """Main interactive loop"""
    print_banner()
    
    # Initialize router
    router = ModelRouter()
    
    # Fix Google model name (workaround for config loading issue)
    if "google:gemini-pro" in router.profiles:
        old_profile = router.profiles.pop("google:gemini-pro")
        router.profiles["google:gemini-1.5-flash"] = old_profile
    
    print(f"⚙️ Initial Strategy: {router.strategy}")
    print(f"⚖️ Weights: Cost={router.weights['cost']:.1%}, Latency={router.weights['latency']:.1%}, Quality={router.weights['quality']:.1%}")
    
    # Check if input is being piped (non-interactive mode)
    import sys
    is_piped = not sys.stdin.isatty()
    
    if is_piped:
        # Non-interactive mode: process single input and exit
        try:
            user_input = input().strip().strip('"').strip("'")
            if user_input:
                # Check if it's a command first
                if user_input.lower() in ['quit', 'exit']:
                    print("\n👋 Goodbye! Thanks for using AgentsIQ!")
                    return
                elif user_input.lower() == 'help':
                    print_help()
                    return
                elif user_input.lower() in ['strategies', 'startegies', 'strategy']:
                    print_strategies()
                    return
                elif user_input.lower() in ['models', 'model']:
                    print_models(router)
                    return
                elif user_input.lower() in ['history', 'hist']:
                    show_history()
                    return
                elif user_input.lower() in ['dashboard', 'dash']:
                    show_dashboard()
                    return
                elif user_input.lower() in ['debug', 'dbg']:
                    show_debug_info()
                    return
                else:
                    # Process as a query
                    result = process_query(router, user_input)
                    if result != "quit":
                        print(f"\n✅ Query Processed!")
        except EOFError:
            pass
        return
    
    while True:
        try:
            user_input = input("\n🔍 Enter query (or 'help'): ").strip().strip('"').strip("'")
            
            if not user_input:
                continue
                
            # Handle commands
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 Goodbye! Thanks for using AgentsIQ!")
                break
            elif user_input.lower() == 'help':
                print_help()
            elif user_input.lower() in ['strategies', 'startegies', 'strategy']:
                print_strategies()
            elif user_input.lower() in ['models', 'model']:
                print_models(router)
            elif user_input.lower() in ['history', 'hist']:
                show_history()
            elif user_input.lower() in ['dashboard', 'dash']:
                show_dashboard()
            elif user_input.lower() in ['debug', 'dbg']:
                show_debug_info()
            elif user_input.lower() in ['select', 'choose']:
                query = input("Enter query for model selection: ").strip()
                if query:
                    selected_model = interactive_model_selection(router, query)
                    if selected_model:
                        # Process query with selected model directly
                        print(f"\n⚡ Processing with selected model: {selected_model}")
                        start_time = time.time()
                        response, confidence = router.call_model(selected_model, query)
                        end_time = time.time()
                        
                        # Record the decision for dashboard tracking
                        from agentsiq.decision_store import record_decision
                        decision_record = {
                            "agent": "InteractiveQueryTool",
                            "role": "User-selected model",
                            "task": query,
                            "chosen": selected_model,
                            "strategy": "user_selected",
                            "latency": end_time - start_time,
                            "quality": confidence,
                            "est_cost_chosen": 0.0,  # Will be calculated if needed
                            "tokens_total_est": len(query.split()) * 2,  # Rough estimate
                            "est_cost_saved_vs_gpt4o": 0.0,
                            "est_cost_saved_vs_next_best": 0.0
                        }
                        record_decision(decision_record)
                        
                        print(f"\n✅ Query Processed!")
                        print(f"   Model Used: {selected_model}")
                        print(f"   Processing Time: {end_time - start_time:.2f}s")
                        print(f"   Confidence: {confidence:.2f}")
                        print(f"   Response: {response}")
            elif user_input.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
            elif user_input.lower().startswith('strategy '):
                new_strategy = user_input.split(' ', 1)[1].lower()
                if new_strategy in ['smart', 'hybrid', 'cheapest', 'fastest']:
                    router.strategy = new_strategy
                    print(f"✅ Strategy changed to: {new_strategy}")
                else:
                    print(f"❌ Invalid strategy. Use: smart, hybrid, cheapest, or fastest")
            else:
                # Process as a query
                result = process_query(router, user_input)
                if result == "quit":
                    print("\n👋 Goodbye! Thanks for using AgentsIQ!")
                    break
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using AgentsIQ!")
            break
        except Exception as e:
            import traceback
            print(f"\n❌ Error: {e}")
            print(f"Full traceback:")
            traceback.print_exc()
            print("Please try again or type 'help' for assistance.")

if __name__ == "__main__":
    main()
