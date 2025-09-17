
import os
from dotenv import load_dotenv
load_dotenv()
def init_agentops():
    api_key=os.getenv("AGENTOPS_API_KEY")
    if not api_key:
        return False
    try:
        import agentops
        agentops.init(api_key)
        return True
    except Exception:
        return False
