#!/usr/bin/env python3
"""
AgentsIQ Ollama Setup Script
Automatically downloads and configures Ollama models for optimal performance
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors gracefully"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        result = subprocess.run("ollama --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is already installed")
            return True
    except:
        pass
    
    print("❌ Ollama is not installed")
    return False

def install_ollama():
    """Install Ollama based on the operating system"""
    import platform
    system = platform.system().lower()
    
    print("🚀 Installing Ollama...")
    
    if system == "linux" or system == "darwin":  # macOS
        cmd = "curl -fsSL https://ollama.ai/install.sh | sh"
        return run_command(cmd, "Installing Ollama")
    elif system == "windows":
        print("📥 Please download Ollama from https://ollama.ai/download")
        print("   After installation, run this script again.")
        return False
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def pull_models():
    """Pull recommended Ollama models"""
    models = [
        ("llama3.1:8b", "Fast, efficient model for general tasks"),
        ("qwen2.5:7b", "High-quality model with excellent performance"),
    ]
    
    print("\n📦 Pulling recommended models...")
    
    for model, description in models:
        print(f"\n🔄 Pulling {model} - {description}")
        if run_command(f"ollama pull {model}", f"Downloading {model}"):
            print(f"✅ {model} ready!")
        else:
            print(f"⚠️  Failed to download {model}, continuing...")
        
        time.sleep(1)  # Brief pause between downloads

def verify_installation():
    """Verify that models are properly installed"""
    print("\n🔍 Verifying installation...")
    
    try:
        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("📋 Installed models:")
            print(result.stdout)
            return True
        else:
            print("❌ Failed to list models")
            return False
    except Exception as e:
        print(f"❌ Error verifying installation: {e}")
        return False

def test_ollama_connection():
    """Test connection to Ollama"""
    print("\n🧪 Testing Ollama connection...")
    
    try:
        # Test with a simple model call
        result = subprocess.run(
            'ollama run llama3.1:8b "Hello, this is a test"',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print("✅ Ollama connection test successful!")
            print("📝 Sample response:", result.stdout[:100] + "..." if len(result.stdout) > 100 else result.stdout)
            return True
        else:
            print("❌ Ollama connection test failed")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Ollama test timed out (this might be normal for first run)")
        return True
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def create_env_example():
    """Create .env.example file with Ollama configuration"""
    env_content = """# AgentsIQ Environment Configuration

# Cloud Model API Keys (optional)
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here
GROK_API_KEY=your_grok_key_here

# Ollama Configuration (for local models)
OLLAMA_URL=http://localhost:11434

# Optional: AgentOps for advanced analytics
AGENTOPS_API_KEY=your_agentops_key_here
"""
    
    env_file = Path(".env.example")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write(env_content)
        print("📝 Created .env.example file")
    else:
        print("📝 .env.example already exists")

def main():
    """Main setup function"""
    print("🚀 AgentsIQ Ollama Setup")
    print("=" * 40)
    
    # Check if Ollama is installed
    if not check_ollama_installed():
        if not install_ollama():
            print("\n❌ Setup failed. Please install Ollama manually and try again.")
            return False
    
    # Pull recommended models
    pull_models()
    
    # Verify installation
    if not verify_installation():
        print("\n⚠️  Installation verification failed, but continuing...")
    
    # Test connection
    test_ollama_connection()
    
    # Create environment file
    create_env_example()
    
    print("\n🎉 Ollama setup completed!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and add your API keys")
    print("2. Run: python examples/benchmark.py")
    print("3. Choose option 1 for comprehensive model comparison")
    print("\n💡 Pro tip: Ollama models are free to use and run locally!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
