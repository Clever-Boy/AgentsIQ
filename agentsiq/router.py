import os, time, random
from dotenv import load_dotenv

# Load API keys from .env (if present)
load_dotenv()

# Lazy imports to avoid hard dependency during mock runs
_openai_client = None
_anthropic_client = None
_gemini_ready = None

def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        try:
            from openai import OpenAI
            _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception:
            _openai_client = False
    return _openai_client

def _get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        try:
            import anthropic
            _anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        except Exception:
            _anthropic_client = False
    return _anthropic_client

def _ensure_gemini():
    global _gemini_ready
    if _gemini_ready is None:
        try:
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            _gemini_ready = True
        except Exception:
            _gemini_ready = False
    return _gemini_ready

class ModelRouter:
    """Routes a task to an appropriate LLM based on strategy and heuristics."""
    def __init__(self, strategy: str = "hybrid"):
        self.strategy = strategy

    def select_model(self, task: str, preferred: str = "") -> str:
        t = (task or "").lower()
        if preferred:
            # allow preferred model to guide choice when it matches strategy
            return preferred

        if self.strategy == "cheapest":
            return "anthropic:claude-3-haiku"
        if self.strategy == "fastest":
            return "google:gemini-pro"

        # hybrid heuristic
        if "code" in t or "implement" in t or "python" in t:
            return "openai:gpt-4o"
        if "summarize" in t or "tl;dr" in t or "summary" in t:
            return "anthropic:claude-3-haiku"
        return "openai:gpt-4o-mini"

    def call_model(self, model_name: str, prompt: str):
        """Call the specified model. Falls back to a mock if SDK/key not available."""
        if model_name.startswith("openai:"):
            client = _get_openai_client()
            model = model_name.split(":", 1)[1]
            if client:
                try:
                    resp = client.chat.completions.create(
                        model=model,
                        messages=[{"role":"user","content":prompt}],
                        temperature=0.2,
                        max_tokens=500
                    )
                    text = resp.choices[0].message.content
                    return text, 0.85
                except Exception:
                    pass
            # Fallback mock
            return f"[OPENAI MOCK {model}] {prompt[:180]}", random.uniform(0.6, 0.9)

        if model_name.startswith("anthropic:"):
            client = _get_anthropic_client()
            model = model_name.split(":", 1)[1]
            if client:
                try:
                    resp = client.messages.create(
                        model=model,
                        max_tokens=500,
                        messages=[{"role":"user","content":prompt}]
                    )
                    # anthropic returns structured content list
                    text = ""
                    try:
                        text = "".join([b.text for b in resp.content])
                    except Exception:
                        text = str(resp)
                    return text, 0.83
                except Exception:
                    pass
            return f"[ANTHROPIC MOCK {model}] {prompt[:180]}", random.uniform(0.6, 0.9)

        if model_name.startswith("google:"):
            ok = _ensure_gemini()
            model = model_name.split(":", 1)[1]
            if ok:
                try:
                    import google.generativeai as genai
                    gm = genai.GenerativeModel(model)
                    resp = gm.generate_content(prompt)
                    text = getattr(resp, "text", None) or (resp.candidates[0].content.parts[0].text if getattr(resp, "candidates", None) else "")
                    return text, 0.8
                except Exception:
                    pass
            return f"[GEMINI MOCK {model}] {prompt[:180]}", random.uniform(0.6, 0.9)

        # Unknown model -> pure mock
        return f"[MOCK {model_name}] {prompt[:180]}", random.uniform(0.6, 0.9)
