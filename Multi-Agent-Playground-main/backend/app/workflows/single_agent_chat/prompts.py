# Single Agent Chat workflow prompts

from ...schemas import AgentDefinition

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
