#!/usr/bin/env python3
"""
AgentsIQ Query Analyzer
======================

A focused tool that analyzes queries and shows:
1. Task traits detection
2. Model recommendations for different strategies
3. Cost, latency, and quality comparisons
4. Interactive model selection

Usage:
    python examples/query_analyzer.py
"""

import os
from agentsiq.router import ModelRouter, _traits, _estimate_tokens, _score

def print_header():
    """Print a clean header"""
    print("🔍 AgentsIQ Query Analyzer")
    print("=" * 50)
    print("Analyze queries and see intelligent model selection!")
    print("=" * 50)

def analyze_traits(query):
    """Analyze and display query traits"""
    traits = _traits(query)
    tokens = _estimate_tokens(query)
    
    print(f"\n📝 Query: {query}")
    print(f"🔢 Estimated Tokens: {tokens}")
    print(f"\n🎯 Detected Traits:")
    
    trait_info = {
        "is_code": ("💻 Code/Programming", "Contains programming concepts or code"),
        "is_summary": ("📋 Summary", "Asks for summarization or TL;DR"),
        "has_math": ("🧮 Math", "Contains mathematical expressions"),
        "is_creative": ("🎨 Creative", "Requires creative writing"),
        "is_analytical": ("🔬 Analytical", "Requires analysis or reasoning"),
        "is_factual": ("📚 Factual", "Asks for factual information")
    }
    
    for trait, (icon, description) in trait_info.items():
        status = "✅" if traits.get(trait, False) else "❌"
        print(f"  {status} {icon} {description}")

def compare_strategies(router, query):
    """Compare different routing strategies"""
    tokens = _estimate_tokens(query)
    traits = _traits(query)
    
    print(f"\n⚖️ Strategy Comparison:")
    print("-" * 70)
    print(f"{'Strategy':<12} {'Model':<25} {'Cost':<8} {'Latency':<8} {'Quality':<8}")
    print("-" * 70)
    
    strategies = [
        ("smart", "Multi-objective optimization"),
        ("hybrid", "Task-specific selection"),
        ("cheapest", "Lowest cost only"),
        ("fastest", "Fastest only")
    ]
    
    for strategy_name, description in strategies:
        original_strategy = router.strategy
        router.strategy = strategy_name
        
        if strategy_name == "cheapest":
            chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["cost"])
        elif strategy_name == "fastest":
            chosen = min(router.profiles.keys(), key=lambda m: router.profiles[m]["latency"])
        elif strategy_name == "hybrid":
            if traits["is_code"]:
                chosen = "openai:gpt-4o"
            elif traits["is_summary"]:
                chosen = "anthropic:claude-3-haiku"
            else:
                chosen = "openai:gpt-4o-mini"
        else:  # smart
            scored = []
            for m in router.profiles.keys():
                s, why = router._score(m, tokens, traits)
                scored.append((m, s, why))
            scored.sort(key=lambda x: x[1])
            chosen = scored[0][0]
        
        profile = router.profiles[chosen]
        print(f"{strategy_name:<12} {chosen:<25} ${profile['cost']:.3f}   {profile['latency']:.2f}s     {profile['quality']:.2f}")
        
        router.strategy = original_strategy

def show_smart_ranking(router, query):
    """Show detailed smart strategy ranking"""
    tokens = _estimate_tokens(query)
    traits = _traits(query)
    
    print(f"\n🧠 Smart Strategy - Model Ranking:")
    print("-" * 80)
    
    # Calculate efficiency scores for all models
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
    
    scored.sort(key=lambda x: x[1], reverse=True)  # Higher efficiency is better
    
    print(f"{'Rank':<4} {'Model':<25} {'Efficiency':<10} {'Cost':<8} {'Latency':<8} {'Quality':<8} {'Provider':<12}")
    print("-" * 90)
    
    for i, (model, efficiency, est_cost, quality) in enumerate(scored, 1):
        profile = router.profiles[model]
        provider = model.split(':')[0].title()
        print(f"{i:<4} {model:<25} {efficiency:.2f}     ${est_cost:.4f}   {profile['latency']:.2f}s     {quality:.2f}     {provider:<12}")

def show_cost_analysis(router, query):
    """Show cost analysis for different models"""
    tokens = _estimate_tokens(query)
    
    print(f"\n💰 Cost Analysis (for {tokens} tokens):")
    print("-" * 60)
    
    # Calculate costs for different models
    costs = []
    for model, profile in router.profiles.items():
        tokens_out = tokens * 0.3  # Estimate 30% output tokens
        tokens_total = tokens + tokens_out
        cost = profile['cost'] * tokens_total / 1000  # Cost per 1K tokens
        costs.append((model, cost, profile))
    
    costs.sort(key=lambda x: x[1])
    
    print(f"{'Model':<25} {'Cost':<12} {'Latency':<8} {'Quality':<8}")
    print("-" * 60)
    
    for model, cost, profile in costs:
        print(f"{model:<25} ${cost:.6f}   {profile['latency']:.2f}s     {profile['quality']:.2f}")

def interactive_model_selection(router, query):
    """Let user interactively select a model"""
    tokens = _estimate_tokens(query)
    traits = _traits(query)
    
    print(f"\n🎯 Interactive Model Selection:")
    print("-" * 50)
    
    # Get top 5 models by efficiency scoring
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
    
    scored.sort(key=lambda x: x[1], reverse=True)  # Higher efficiency is better
    top_models = scored[:5]
    
    print("Top 5 recommended models:")
    for i, (model, efficiency, est_cost, quality) in enumerate(top_models, 1):
        profile = router.profiles[model]
        print(f"{i}. {model} (Efficiency: {efficiency:.2f}, Cost: ${est_cost:.4f}, Latency: {profile['latency']:.2f}s)")
    
    while True:
        try:
            choice = input(f"\nSelect model (1-{len(top_models)}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(top_models):
                selected_model = top_models[choice_idx][0]
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

def main():
    """Main interactive loop"""
    print_header()
    
    router = ModelRouter()
    
    while True:
        try:
            query = input("\n🔍 Enter your query (or 'quit' to exit): ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            # Analyze the query
            analyze_traits(query)
            
            # Compare strategies
            compare_strategies(router, query)
            
            # Show smart ranking
            show_smart_ranking(router, query)
            
            # Show cost analysis
            show_cost_analysis(router, query)
            
            # Interactive model selection
            selected = interactive_model_selection(router, query)
            
            if selected:
                print(f"\n🚀 You selected: {selected}")
                print("This model would be used to process your query!")
            
            print("\n" + "="*50)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Please try again.")

if __name__ == "__main__":
    main()
