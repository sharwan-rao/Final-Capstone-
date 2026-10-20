# Planner Executor workflow prompts

from ...schemas import AgentDefinition


# Planner prompt - decomposes user request into tasks
PLAN_TASKS_PROMPT = """You are a planning module.
Decompose the user request into at most {max_tasks} executable tasks.
{multi_hint}
{agent_catalog}
Return ONLY a JSON array of strings.
User request: {user_input}"""


def build_plan_tasks_prompt(
    user_input: str,
    max_tasks: int = 4,
    force_multi: bool = False,
    agents: list[AgentDefinition] | None = None,
) -> str:
    """Build the planner prompt."""
    multi_hint = (
        "Prefer at least 2 tasks when the request includes multiple intents."
        if force_multi
        else "Use the minimum number of tasks needed."
    )
    
    agent_catalog = ""
    if agents:
        catalog_lines = "\n".join(
            f"- name={agent.name}; description={agent.description}"
            for agent in agents
        )
        agent_catalog = (
            "Available specialists:\n"
            f"{catalog_lines}\n"
            "Plan tasks so they map clearly onto the available specialists.\n"
            "When the request reasonably spans product/design/engineering, reflect that in the task split.\n"
            "Prefer task wording that makes the best specialist obvious.\n"
        )
    
    return PLAN_TASKS_PROMPT.format(
        user_input=user_input,
        max_tasks=max_tasks,
        multi_hint=multi_hint,
        agent_catalog=agent_catalog,
    )


# Keywords that indicate multi-task requests
MULTI_HINT_KEYWORDS = (
    " and ",
    " also ",
    " then ",
    " additionally ",
    " furthermore ",
    " as well as ",
    " next ",
    " finally ",
)


def should_force_multi(user_input: str) -> bool:
    """Check if the user input suggests multiple tasks."""
    return any(kw in user_input.lower() for kw in MULTI_HINT_KEYWORDS)


# Fallback planner - simple task splitting by punctuation
def fallback_plan_tasks(user_input: str, max_tasks: int = 4) -> list[str]:
    """Fallback task planning by simple splitting."""
    # Split by common separators
    separators = [";", "\n", " and ", " then ", ". "]
    tasks = [user_input]
    
    for sep in separators:
        new_tasks = []
        for task in tasks:
            new_tasks.extend(task.split(sep))
        if len(new_tasks) > len(tasks):
            tasks = new_tasks
            break
    
    # Clean up and limit
    tasks = [t.strip() for t in tasks if t.strip()]
    return tasks[:max_tasks]


# Router prompt - same as router_specialists
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

