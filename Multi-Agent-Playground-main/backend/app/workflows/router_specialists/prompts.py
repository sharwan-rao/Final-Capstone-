# Router Specialists workflow prompts

from ...schemas import AgentDefinition


# Router prompt - used to select the best specialist agent
ROUTER_PROMPT = """You are a workflow router. Select the specialist agent best suited to handle the user request from the options below.
Return ONLY a single line in the format: agent_id|reason
Available agents:
{agent_catalog}
User request: {user_input}"""


def build_router_prompt(user_input: str, agents: list[AgentDefinition]) -> str:
    """Build the router prompt with agent catalog."""
    catalog = "\n".join(
        f"- id={agent.id}; name={agent.name}; description={agent.description}"
        for agent in agents
    )
    return ROUTER_PROMPT.format(
        user_input=user_input,
        agent_catalog=catalog,
    )


# Fallback route by keywords
FALLBACK_ROUTE_KEYWORDS: dict[str, list[str]] = {
    "architecture": ["architecture", "design", "boundary", "module", "system design"],
    "writing": ["write", "summarize", "documentation", "document", "rewrite", "explain"],
    "learning": ["learn", "roadmap", "how to learn", "advice", "steps", "guide"],
}


def fallback_route_keyword(user_input: str, agents: list[AgentDefinition]) -> tuple[str, str] | None:
    """Fallback routing by keyword matching."""
    input_lower = user_input.lower()
    for agent_id, keywords in FALLBACK_ROUTE_KEYWORDS.items():
        # Check if any keyword matches
        if any(kw.lower() in input_lower for kw in keywords):
            # Find matching agent
            for agent in agents:
                if agent.id == agent_id or agent_id in agent.name.lower():
                    return agent.id, f"keyword match: {keywords}"
    return None


# Finalizer prompt - same as single_agent_chat
FINALIZE_PROMPT = """You are a workflow finalizer. Based on the user's original request and the specialist's answer,
output the final user-facing response, keeping it within 6 sentences.
User request: {user_input}
Specialist: {agent_name}
Specialist response: {specialist_answer}"""


def build_finalize_prompt(
    user_input: str,
    agent: AgentDefinition,
    specialist_answer: str,
) -> str:
    return FINALIZE_PROMPT.format(
        user_input=user_input,
        agent_name=agent.name,
        specialist_answer=specialist_answer,
    )


FALLBACK_FINALIZE_RESPONSE = (
    "The system routed your request to {agent_name}.\n"
    "{agent_name}'s response is as follows:\n{answer}"
)


def build_fallback_response(agent_name: str, answer: str) -> str:
    return FALLBACK_FINALIZE_RESPONSE.format(
        agent_name=agent_name,
        answer=answer,
    )
