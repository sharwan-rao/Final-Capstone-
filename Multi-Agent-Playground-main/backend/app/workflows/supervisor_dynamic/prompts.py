# Supervisor Dynamic workflow prompts

from ...schemas import AgentDefinition


# Router prompt - same as other workflows
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


FALLBACK_ROUTE_KEYWORDS: dict[str, list[str]] = {
    "architecture": ["architecture", "design", "boundary", "module", "system design"],
    "writing": ["write", "summarize", "documentation", "document", "rewrite", "explain"],
    "learning": ["learn", "roadmap", "how to learn", "advice", "steps", "guide"],
}


def fallback_route_keyword(user_input: str, agents: list[AgentDefinition]) -> tuple[str, str] | None:
    """Fallback routing by keyword matching."""
    input_lower = user_input.lower()
    for agent_id, keywords in FALLBACK_ROUTE_KEYWORDS.items():
        if any(kw.lower() in input_lower for kw in keywords):
            for agent in agents:
                if agent.id == agent_id or agent_id in agent.name.lower():
                    return agent.id, f"keyword match: {keywords}"
    return None


# Supervisor review prompt - decides whether to continue delegation
SUPERVISOR_REVIEW_PROMPT = """You are a supervisor loop controller.
Given the original user request and worker reports, decide whether to continue delegation.
Respond with JSON only in this shape:
{{"continue": true/false, "next_focus_task": "<string>", "reason": "<string>"}}
Rules:
- If current output is sufficient and coherent, set continue=false.
- If key requirements are missing, set continue=true and provide the next focus task.
- Current cycle: {cycle}, max cycles: {max_cycles}.

User request:
{user_input}

Recent reports:
{report_block}"""


def build_supervisor_review_prompt(
    user_input: str,
    reports: list[str],
    cycle: int,
    max_cycles: int,
) -> str:
    """Build the supervisor review prompt."""
    recent_reports = reports[-3:] if reports else []
    report_block = "\n\n".join(recent_reports) if recent_reports else "(no reports yet)"
    return SUPERVISOR_REVIEW_PROMPT.format(
        user_input=user_input,
        report_block=report_block,
        cycle=cycle,
        max_cycles=max_cycles,
    )


# Fallback keywords for supervisor
SUPERVISOR_FALLBACK_KEYWORDS_UNRESOLVED = (
    "todo",
    "unknown",
    "risk",
    "assumption",
    "unresolved",
    "missing",
    "pending",
    "incomplete",
)

SUPERVISOR_FALLBACK_KEYWORDS_COMPLETE = (
    "final",
    "complete",
    "done",
    "conclusion",
    "completed",
    "finished",
    "resolved",
)


def fallback_supervisor_review_decision(
    user_input: str,
    reports: list[str],
    cycle: int,
    max_cycles: int,
) -> tuple[bool, str, str]:
    """Fallback supervisor decision based on keywords."""
    if cycle >= max_cycles:
        return False, "", "Reached max cycle limit."
    
    if not reports:
        return True, "Start with the first task.", "No reports yet."
    
    latest = reports[-1].lower()
    unresolved_markers = SUPERVISOR_FALLBACK_KEYWORDS_UNRESOLVED
    complete_markers = SUPERVISOR_FALLBACK_KEYWORDS_COMPLETE
    
    if any(token in latest for token in unresolved_markers):
        return True, "Continue detailing actionable solutions for unresolved items.", "Fallback: latest report indicates unresolved items."
    if any(token in latest for token in complete_markers):
        return False, "", "Fallback: latest report appears complete."
    return False, "", "Fallback: no strong signal to continue."


# Finalizer prompt
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
