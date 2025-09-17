def check_permission(agent, tool_name: str):
    """Simple RBAC: agent.allowed_tools lists allowed tool names."""
    return tool_name in getattr(agent, 'allowed_tools', [])
