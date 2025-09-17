def check_permission(agent, tool_name: str) -> bool:
    return tool_name in getattr(agent, "allowed_tools", [])
