#!/usr/bin/env python3
"""
AgentsIQ Model Selector
======================

An enhanced interactive tool that:
1. Shows all available models with detailed summaries
2. Allows strategy selection (smart, hybrid, cheapest, fastest)
3. Provides interactive model selection with recommendations
4. Processes queries with the selected model

Usage:
    python examples/model_selector.py
"""

import os
import time
from datetime import datetime
from agentsiq.router import ModelRouter, _traits, _estimate_tokens
from agentsiq.agent import Agent

def print_banner():
    """Print a welcome banner"""
    print("=" * 80)
    print("🎯 AgentsIQ Model Selector")
    print("=" * 80)
    print("Choose your strategy and model for intelligent query processing!")
    print("=" * 80)

def show_all_models(router):
    """Show all available models with detailed summaries"""
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

def show_strategies():
    """Show available strategies with descriptions"""
    print("\n⚙️ Available Strategies:")
    print("-" * 60)
    
    strategies = {
        "smart": {
            "name": "Smart (Multi-objective)",
            "description": "Balances cost, latency, and quality using optimization",
            "best_for": "Most use cases, automatic optimization"
        },
        "hybrid": {
            "name": "Hybrid (Task-specific)",
            "description": "Chooses models based on task type",
            "best_for": "Code→GPT-4o, Summary→Claude, Other→GPT-4o-mini"
        },
        "cheapest": {
            "name": "Cheapest",
            "description": "Always selects the lowest cost model",
            "best_for": "Budget-conscious applications"
        },
        "fastest": {
            "name": "Fastest",
            "description": "Always selects the fastest model",
            "best_for": "Real-time applications requiring speed"
        }
    }
    
    for strategy, info in strategies.items():
        print(f"  {strategy.upper():<8}: {info['name']}")
        print(f"           {info['description']}")
        print(f"           Best for: {info['best_for']}")
        print()

def select_strategy(router):
    """Let user select a strategy"""
    while True:
        print("\n🎯 Select Strategy:")
        print("1. Smart (Multi-objective optimization)")
        print("2. Hybrid (Task-specific selection)")
        print("3. Cheapest (Lowest cost)")
        print("4. Fastest (Lowest latency)")
        print("5. Show strategy details")
        
        try:
            choice = input("\nEnter choice (1-5): ").strip()
            
            if choice == "1":
                router.strategy = "smart"
                print("✅ Selected: Smart strategy")
                break
            elif choice == "2":
                router.strategy = "hybrid"
                print("✅ Selected: Hybrid strategy")
                break
            elif choice == "3":
                router.strategy = "cheapest"
                print("✅ Selected: Cheapest strategy")
                break
            elif choice == "4":
                router.strategy = "fastest"
                print("✅ Selected: Fastest strategy")
                break
            elif choice == "5":
                show_strategies()
            else:
                print("❌ Invalid choice. Please enter 1-5.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return True

def analyze_query(query):
    """Analyze query and show traits"""
    traits = _traits(query)
    tokens = _estimate_tokens(query)
    
    print(f"\n🔍 Query Analysis:")
    print(f"  Query: {query}")
    print(f"  Estimated Tokens: {tokens}")
    print(f"  Detected Traits:")
    
    trait_descriptions = {
        "is_code": "💻 Code/Programming",
        "is_summary": "📋 Summary",
        "has_math": "🧮 Math",
        "is_creative": "🎨 Creative",
        "is_analytical": "🔬 Analytical",
        "is_factual": "📚 Factual"
    }
    
    for trait, icon in trait_descriptions.items():
        status = "✅" if traits.get(trait, False) else "❌"
        print(f"    {status} {icon}")
    
    return traits, tokens

def get_model_recommendations(router, query, traits, tokens):
    """Get model recommendations based on strategy"""
    print(f"\n🎯 Model Recommendations for '{router.strategy}' strategy:")
    print("-" * 80)
    
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
        
        print(f"{'Rank':<4} {'Model':<25} {'Efficiency':<10} {'Cost':<8} {'Latency':<8} {'Quality':<8}")
        print("-" * 80)
        
        for i, (model, efficiency, est_cost, quality) in enumerate(scored[:5], 1):
            profile = router.profiles[model]
            print(f"{i:<4} {model:<25} {efficiency:.2f}     ${est_cost:.4f}   {profile['latency']:.2f}s     {quality:.2f}")
        
        return [model for model, _, _, _ in scored[:5]]
    
    elif router.strategy == "hybrid":
        if traits["is_code"]:
            chosen = "openai:gpt-4o"
        elif traits["is_summary"]:
            chosen = "anthropic:claude-3-haiku"
        else:
            chosen = "openai:gpt-4o-mini"
        
        profile = router.profiles[chosen]
        print(f"Selected: {chosen}")
        print(f"Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f}")
        return [chosen]
    
    elif router.strategy == "cheapest":
        chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["cost"])
        profile = router.profiles[chosen]
        print(f"Selected: {chosen}")
        print(f"Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f}")
        return [chosen]
    
    elif router.strategy == "fastest":
        chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["latency"])
        profile = router.profiles[chosen]
        print(f"Selected: {chosen}")
        print(f"Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f}")
        return [chosen]

def select_model_interactive(router, recommendations):
    """Let user select a model interactively"""
    print(f"\n🎯 Select Model:")
    print("-" * 50)
    
    if len(recommendations) == 1:
        print(f"Auto-selected: {recommendations[0]}")
        return recommendations[0]
    
    print("Recommended models:")
    for i, model in enumerate(recommendations, 1):
        profile = router.profiles[model]
        print(f"{i}. {model} (Cost: ${profile['cost']:.3f}, Latency: {profile['latency']:.2f}s, Quality: {profile['quality']:.2f})")
    
    # Show all models option
    print(f"{len(recommendations) + 1}. Show all models")
    
    while True:
        try:
            choice = input(f"\nSelect model (1-{len(recommendations) + 1}): ").strip()
            choice_idx = int(choice) - 1
            
            if 0 <= choice_idx < len(recommendations):
                selected = recommendations[choice_idx]
                print(f"✅ Selected: {selected}")
                return selected
            elif choice_idx == len(recommendations):
                show_all_models(router)
                # Let user select from all models
                while True:
                    try:
                        model_choice = input(f"\nSelect model (1-{len(router.profiles)}): ").strip()
                        model_idx = int(model_choice) - 1
                        if 0 <= model_idx < len(router.profiles):
                            selected = list(router.profiles.keys())[model_idx]
                            print(f"✅ Selected: {selected}")
                            return selected
                        else:
                            print("❌ Invalid choice.")
                    except ValueError:
                        print("❌ Please enter a number.")
                    except KeyboardInterrupt:
                        return None
            else:
                print("❌ Invalid choice. Please try again.")
        except ValueError:
            print("❌ Please enter a number.")
        except KeyboardInterrupt:
            return None

def process_query(router, query, selected_model):
    """Process the query with the selected model"""
    print(f"\n⚡ Processing Query:")
    print(f"  Query: {query}")
    print(f"  Model: {selected_model}")
    print(f"  Strategy: {router.strategy}")
    print("-" * 60)
    
    # Create agent with selected model
    agent = Agent(
        name="QueryProcessor",
        role="Processes user queries",
        model=selected_model,
        allowed_tools=[]
    )
    
    start_time = time.time()
    result = agent.act(query, router=router)
    end_time = time.time()
    
    print(f"\n✅ Query Processed Successfully!")
    print(f"   Model Used: {result['model_used']}")
    print(f"   Processing Time: {end_time - start_time:.2f}s")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"\n📝 Response:")
    print(f"   {result['response']}")
    
    return result

def main():
    """Main interactive loop"""
    print_banner()
    
    # Initialize router
    router = ModelRouter()
    print(f"⚙️ Current Strategy: {router.strategy}")
    print(f"⚖️ Weights: Cost={router.weights['cost']:.1%}, Latency={router.weights['latency']:.1%}, Quality={router.weights['quality']:.1%}")
    
    while True:
        try:
            print("\n" + "="*80)
            query = input("\n🔍 Enter your query (or 'quit' to exit): ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! Thanks for using AgentsIQ!")
                break
            
            # Analyze the query
            traits, tokens = analyze_query(query)
            
            # Show all models
            show_all_models(router)
            
            # Select strategy
            if not select_strategy(router):
                break
            
            # Get recommendations
            recommendations = get_model_recommendations(router, query, traits, tokens)
            
            # Select model
            selected_model = select_model_interactive(router, recommendations)
            if not selected_model:
                continue
            
            # Process query
            result = process_query(router, query, selected_model)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using AgentsIQ!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
