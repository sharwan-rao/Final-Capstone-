from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


WorkflowType = Literal[
    "router_specialists",
    "planner_executor",
    "supervisor_dynamic",
    "single_agent_chat",
    "peer_handoff",
]
BuiltinCapability = Literal[
    "filesystem",
    "fs_list",
    "fs_read",
    "fs_write",
]
TraceEventType = Literal[
    "run_started",
    "node_entered",
    "node_exited",
    "route_selected",
    "message_generated",
    "state_updated",
    "run_finished",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SkillDefinitionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=200)
    instruction: str = Field(min_length=1)


class SkillDefinition(SkillDefinitionCreate):
    id: str
    source_provider: str | None = None
    source_skill_id: str | None = None
    tool: dict[str, Any] | None = None
    local_path: str | None = None
    runtime_preflight: dict[str, Any] | None = None


class SkillSyncRequest(BaseModel):
    provider: Literal["skillhub"] = "skillhub"
    query: str | None = Field(default="search", max_length=80)
    limit: int = Field(default=40, ge=1, le=100)


class SkillSyncResponse(BaseModel):
    provider: str
    query: str
    fetched: int
    imported: int
    updated: int


class SkillInstallResponse(BaseModel):
    skill_id: str
    skill_name: str
    source_provider: str | None = None
    source_skill_id: str | None = None
    downloaded_files: int = 0
    tool_enabled: bool = False
    message: str


class AgentDefinitionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=200)
    system_prompt: str = Field(min_length=1)
    model: str | None = None
    skill_ids: list[str] = Field(default_factory=list)
    builtin_capabilities: list[BuiltinCapability] = Field(default_factory=list)


class AgentDefinition(AgentDefinitionCreate):
    id: str


class AgentDefinitionUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=200)
    system_prompt: str = Field(min_length=1)
    model: str | None = None
    skill_ids: list[str] = Field(default_factory=list)
    builtin_capabilities: list[BuiltinCapability] = Field(default_factory=list)


class WorkflowDefinitionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: WorkflowType
    specialist_agent_ids: list[str] = Field(default_factory=list)
    router_prompt: str = Field(
        default="You are a workflow router. Pick the best specialist based on user intent."
    )
    finalizer_enabled: bool = True


class WorkflowDefinition(WorkflowDefinitionCreate):
    id: str


class WorkflowDefinitionUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: WorkflowType
    specialist_agent_ids: list[str] = Field(default_factory=list)
    router_prompt: str = Field(
        default="You are a workflow router. Pick the best specialist based on user intent."
    )
    finalizer_enabled: bool = True


class WorkflowTemplate(BaseModel):
    type: WorkflowType
    label: str
    description: str
    required_agent_count: int


class WorkflowNode(BaseModel):
    id: str
    label: str
    kind: Literal["start", "logic", "agent", "final", "end", "group"]
    parent_id: str | None = None


class WorkflowEdge(BaseModel):
    source: str
    target: str
    label: str | None = None


class WorkflowGraph(BaseModel):
    nodes: list[WorkflowNode]
    edges: list[WorkflowEdge]


class TraceEvent(BaseModel):
    type: TraceEventType
    title: str
    detail: str
    at: str = Field(default_factory=utc_now_iso)
    payload: dict[str, Any] = Field(default_factory=dict)


class RunArtifacts(BaseModel):
    route_agent_id: str | None = None
    route_agent_name: str | None = None
    route_reason: str | None = None
    specialist_answer: str | None = None
    final_answer: str | None = None


class WorkflowRunRequest(BaseModel):
    workflow_id: str
    user_input: str = Field(min_length=1)
    conversation_id: str | None = None


class WorkflowRunResponse(BaseModel):
    workflow_id: str
    user_input: str
    assistant_message: str
    trace: list[TraceEvent]
    graph: WorkflowGraph
    artifacts: RunArtifacts
    conversation_id: str | None = None


class BenchmarkRunRequest(BaseModel):
    """Run one prompt through several workflows without changing chat history."""

    workflow_ids: list[str] = Field(min_length=1, max_length=8)
    user_input: str = Field(min_length=1, max_length=12_000)


class BenchmarkMetrics(BaseModel):
    duration_ms: int
    trace_events: int
    nodes_visited: int
    agent_steps: int
    tool_events: int
    handoffs: int


class BenchmarkResult(BaseModel):
    workflow_id: str
    workflow_name: str
    workflow_type: WorkflowType
    status: Literal["completed", "failed"]
    metrics: BenchmarkMetrics
    assistant_message: str | None = None
    trace: list[TraceEvent] = Field(default_factory=list)
    graph: WorkflowGraph | None = None
    artifacts: RunArtifacts | None = None
    error: str | None = None


class BenchmarkRunResponse(BaseModel):
    user_input: str
    started_at: str = Field(default_factory=utc_now_iso)
    results: list[BenchmarkResult]


class ConversationCreate(BaseModel):
    workflow_id: str = Field(min_length=1)


class Conversation(ConversationCreate):
    id: str
    title: str | None = None
    created_at: str
    updated_at: str


class Message(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    agent_name: str | None = None
    created_at: str


class ConversationDetail(Conversation):
    messages: list[Message] = Field(default_factory=list)


class ModelProfile(BaseModel):
    id: str
    provider: str = "custom"
    name: str = "Default"
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"


class EnvVarEntry(BaseModel):
    key: str = Field(min_length=1)
    value: str = ""


class AppSettings(BaseModel):
    model_profiles: list[ModelProfile] = Field(default_factory=list)
    active_model_profile_id: str | None = None
    env_vars: list[EnvVarEntry] = Field(default_factory=list)
    env_path: str = ""
