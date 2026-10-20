<script setup>
import { computed, inject, nextTick, ref, watch } from "vue";
import {
  Bot,
  BrainCircuit,
  ChevronRight,
  GitBranch,
  Sparkles,
  Terminal,
  Wrench,
} from "lucide-vue-next";
import { I18N_KEY } from "../i18n";

const props = defineProps({
  trace: { type: Array, default: () => [] },
  playing: { type: Boolean, default: false },
});

const i18n = inject(I18N_KEY, null);
const t = i18n?.t || ((key) => key);
const locale = i18n?.locale;
const traceRef = ref(null);
const traceMode = ref("simple");
const expanded = ref({});

const NODE_LABELS = {
  start: "System",
  end: "System",
  router: "Router",
  finalize: "Finalizer",
  planner_core: "Planner",
  planner_validator: "Plan Validator",
  task_dispatcher: "Task Dispatcher",
  synthesizer: "Synthesizer",
  supervisor_intake: "Supervisor",
  delegation_policy: "Supervisor",
  supervisor_review: "Supervisor",
  first_owner_router: "Router",
  peer_pool: "Peer Pool",
};

function events() {
  return Array.isArray(props.trace) ? props.trace : [];
}

function humanize(value) {
  return String(value || "")
    .replace(/^agent_/, "")
    .replace(/[_-]+/g, " ")
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

// Map agent node ids (agent_b7e9…) to the real agent name, mined from event detail text.
const agentNames = computed(() => {
  const map = {};
  for (const event of events()) {
    const payload = event?.payload || {};
    const detail = String(event?.detail || "").trim();
    if (payload.agent_name && payload.node_id) {
      map[payload.node_id] = String(payload.agent_name).trim();
    }
    const nodeId = String(payload.node_id || "");
    if (nodeId.startsWith("agent_") && !map[nodeId]) {
      const m = detail.match(/^(.+?)\s+(?:is|was|has|returned|completed|reported|finished)\b/i);
      if (m?.[1]) map[nodeId] = m[1].trim();
    }
    const nextId = String(payload.next_node_id || "");
    if (nextId.startsWith("agent_") && !map[nextId]) {
      const m = detail.match(/selected\s+(.+?)\.?$/i);
      if (m?.[1]) map[nextId] = m[1].trim();
    }
  }
  return map;
});

function label(nodeId) {
  const id = String(nodeId || "").trim();
  if (!id) return "System";
  if (agentNames.value[id]) return agentNames.value[id];
  if (NODE_LABELS[id]) return NODE_LABELS[id];
  if (id.startsWith("agent_")) return humanize(id) || "Agent";
  return humanize(id);
}

function actorOf(event) {
  const payload = event?.payload || {};
  const nodeId = String(payload.node_id || "");
  if (payload.agent_name) return { key: `a:${payload.agent_name}`, name: String(payload.agent_name), kind: "agent" };
  if (nodeId.startsWith("agent_")) return { key: `n:${nodeId}`, name: label(nodeId), kind: "agent" };
  if (nodeId === "router" || nodeId.includes("router")) return { key: `n:${nodeId}`, name: label(nodeId), kind: "logic" };
  if (nodeId === "finalize" || nodeId === "synthesizer") return { key: `n:${nodeId}`, name: label(nodeId), kind: "finalize" };
  if (nodeId) return { key: `n:${nodeId}`, name: label(nodeId), kind: "logic" };
  return { key: "system", name: "System", kind: "system" };
}

function shortPath(value) {
  const text = String(value || "").trim();
  if (text.length <= 48) return text;
  return `…${text.slice(-46)}`;
}

function toolTarget(row) {
  if (row.files?.length) return row.files.join(", ");
  const preview = String(row.preview || "");
  const m = preview.match(/(?:Wrote file|Directory ready|Read file|Moved)[:\s]+([^\s(]+)/i);
  return m?.[1] || "";
}

// Build actor-grouped rows; collapse the Started/Output/Finished trio of one tool call into a single row.
const groups = computed(() => {
  const out = [];
  let current = null;
  let toolRows = {};

  const pushRow = (row) => {
    if (!current) {
      current = { key: "system", name: "System", kind: "system", rows: [] };
      out.push(current);
    }
    current.rows.push(row);
  };

  events().forEach((event, index) => {
    const type = String(event?.type || "");
    const title = String(event?.title || "");
    const payload = event?.payload || {};
    const at = event?.at || "";
    const actor = actorOf(event);

    if (!current || current.key !== actor.key) {
      current = { ...actor, rows: [] };
      toolRows = {};
      out.push(current);
    }

    // Skip bare node enter/exit — the group header already names the actor.
    if (type === "node_entered" || type === "node_exited") return;

    const callId = String(payload.tool_call_id || "");
    const toolName = String(payload.tool_name || "");

    if (toolName && callId) {
      let row = toolRows[callId];
      if (!row) {
        row = {
          id: `tool-${callId}`,
          kind: "tool",
          tool: toolName,
          status: { label: "running", tone: "running" },
          at,
          files: [],
          preview: "",
          json: "",
        };
        toolRows[callId] = row;
        pushRow(row);
      }
      if (Array.isArray(payload.generated_files) && payload.generated_files.length) {
        row.files = payload.generated_files;
      }
      if (payload.preview) row.preview = String(payload.preview);
      if (payload.duration_ms != null) row.duration = payload.duration_ms;
      if (title === "Tool Finished" || payload.ok === true) row.status = { label: "ok", tone: "ok" };
      if (title === "Tool Failed" || title === "Tool Unavailable" || payload.ok === false) {
        row.status = { label: "failed", tone: "issue" };
        row.detail = String(event?.detail || "").trim();
      }
      if (title === "Tool Finished" || title === "Tool Failed") {
        row.json = JSON.stringify(payload, null, 2);
      }
      return;
    }

    // Plain event row.
    pushRow({
      id: `ev-${index}`,
      kind: "event",
      action: title || humanize(type) || "Event",
      detail: String(event?.detail || "").trim(),
      cycle: payload.cycle,
      at,
      json: payload && Object.keys(payload).length ? JSON.stringify(payload, null, 2) : "",
    });
  });

  return out;
});

const flatEvents = computed(() =>
  events().map((event, index) => ({
    id: `f-${index}`,
    action: String(event?.title || "") || humanize(String(event?.type || "")) || "Event",
    actor: actorOf(event).name,
    detail: String(event?.detail || "").trim(),
    at: event?.at || "",
    json:
      event?.payload && Object.keys(event.payload).length
        ? JSON.stringify(event.payload, null, 2)
        : "",
  })),
);

const hasTrace = computed(() => events().length > 0);

function toggle(id) {
  expanded.value = { ...expanded.value, [id]: !expanded.value[id] };
}

function formatTime(iso) {
  try {
    const l = locale?.value === "zh-CN" ? "zh-CN" : "en-GB";
    return new Date(iso).toLocaleTimeString(l, {
      hour12: false,
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return iso;
  }
}

function actorIcon(kind) {
  if (kind === "agent") return Bot;
  if (kind === "logic") return BrainCircuit;
  if (kind === "finalize") return Sparkles;
  return GitBranch;
}

watch(
  () => [events().length, traceMode.value],
  async () => {
    if (!traceRef.value) return;
    await nextTick();
    traceRef.value.scrollTop = traceRef.value.scrollHeight;
  },
);
</script>

<template>
  <section class="glass-panel trace-shell">
    <header class="run-panel-header">
      <h3 class="run-panel-title">
        <Terminal :size="18" class="text-slate-400" />
        Trace
      </h3>
      <div class="trace-toolbar">
        <div class="trace-mode-switch" role="tablist" aria-label="Trace mode">
          <button
            type="button"
            class="trace-mode-button"
            :class="{ active: traceMode === 'simple' }"
            @click="traceMode = 'simple'"
          >
            {{ t("trace.showKey") }}
          </button>
          <button
            type="button"
            class="trace-mode-button"
            :class="{ active: traceMode === 'detail' }"
            @click="traceMode = 'detail'"
          >
            {{ t("trace.showAll") }}
          </button>
        </div>
        <span class="chip chip-green">{{ playing ? t("trace.playing") : t("trace.live") }}</span>
      </div>
    </header>

    <div v-if="hasTrace" ref="traceRef" class="trace-list tv-list">
      <!-- Simple: actor groups, collapsed tool calls -->
      <template v-if="traceMode === 'simple'">
        <article v-for="(group, gi) in groups" :key="`${group.key}-${gi}`" class="tv-group">
          <div class="tv-group-head">
            <component :is="actorIcon(group.kind)" :size="15" class="tv-group-icon" />
            <strong>{{ group.name }}</strong>
          </div>

          <div class="tv-rows">
            <template v-for="row in group.rows" :key="row.id">
              <!-- Tool call row -->
              <div v-if="row.kind === 'tool'" class="tv-row">
                <span class="tv-status" :class="`tv-status-${row.status.tone}`">
                  {{ row.status.tone === "ok" ? "✓" : row.status.tone === "issue" ? "✕" : "•" }}
                </span>
                <div class="tv-row-main">
                  <div class="tv-row-line">
                    <Wrench :size="12" class="tv-row-tool-icon" />
                    <span class="tv-row-tool">{{ row.tool }}</span>
                    <span v-if="toolTarget(row)" class="tv-row-target">{{ shortPath(toolTarget(row)) }}</span>
                    <span v-if="row.duration != null" class="tv-row-dim">{{ row.duration }}ms</span>
                    <span class="tv-row-time">{{ formatTime(row.at) }}</span>
                    <button v-if="row.json" type="button" class="tv-toggle" @click="toggle(row.id)">
                      <ChevronRight :size="12" :class="{ 'tv-toggle-open': expanded[row.id] }" />
                    </button>
                  </div>
                  <p v-if="row.detail" class="tv-row-detail">{{ row.detail }}</p>
                  <pre v-if="row.json && expanded[row.id]" class="tv-json">{{ row.json }}</pre>
                </div>
              </div>

              <!-- Plain event row -->
              <div v-else class="tv-row">
                <span class="tv-status tv-status-dot">•</span>
                <div class="tv-row-main">
                  <div class="tv-row-line">
                    <span class="tv-row-action">{{ row.action }}</span>
                    <span v-if="row.cycle" class="tv-row-dim">cycle {{ row.cycle }}</span>
                    <span class="tv-row-time">{{ formatTime(row.at) }}</span>
                    <button v-if="row.json" type="button" class="tv-toggle" @click="toggle(row.id)">
                      <ChevronRight :size="12" :class="{ 'tv-toggle-open': expanded[row.id] }" />
                    </button>
                  </div>
                  <p v-if="row.detail" class="tv-row-detail">{{ row.detail }}</p>
                  <pre v-if="row.json && expanded[row.id]" class="tv-json">{{ row.json }}</pre>
                </div>
              </div>
            </template>
          </div>
        </article>
      </template>

      <!-- Detail: every event, JSON behind a toggle -->
      <template v-else>
        <div v-for="row in flatEvents" :key="row.id" class="tv-row tv-row-flat">
          <span class="tv-status tv-status-dot">•</span>
          <div class="tv-row-main">
            <div class="tv-row-line">
              <span class="tv-row-action">{{ row.action }}</span>
              <span class="tv-row-dim">{{ row.actor }}</span>
              <span class="tv-row-time">{{ formatTime(row.at) }}</span>
              <button v-if="row.json" type="button" class="tv-toggle" @click="toggle(row.id)">
                <ChevronRight :size="12" :class="{ 'tv-toggle-open': expanded[row.id] }" />
              </button>
            </div>
            <p v-if="row.detail" class="tv-row-detail">{{ row.detail }}</p>
            <pre v-if="row.json && expanded[row.id]" class="tv-json">{{ row.json }}</pre>
          </div>
        </div>
      </template>
    </div>
    <div v-else class="trace-empty">{{ t("trace.empty") }}</div>
  </section>
</template>

<style scoped>
.tv-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 4px 2px;
}
.tv-group-head {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  letter-spacing: 0.02em;
  opacity: 0.85;
  margin-bottom: 4px;
}
.tv-group-icon {
  opacity: 0.7;
}
.tv-rows {
  display: flex;
  flex-direction: column;
  gap: 2px;
  border-left: 1px solid rgba(148, 163, 184, 0.25);
  padding-left: 10px;
  margin-left: 6px;
}
.tv-row {
  display: flex;
  gap: 8px;
  padding: 4px 0;
  font-size: 12px;
}
.tv-row-flat {
  border-bottom: 1px solid rgba(148, 163, 184, 0.12);
}
.tv-status {
  flex-shrink: 0;
  width: 14px;
  text-align: center;
  line-height: 1.4;
}
.tv-status-ok {
  color: #4ade80;
}
.tv-status-issue {
  color: #f87171;
}
.tv-status-running,
.tv-status-dot {
  color: #94a3b8;
}
.tv-row-main {
  flex: 1;
  min-width: 0;
}
.tv-row-line {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.tv-row-tool-icon {
  opacity: 0.6;
}
.tv-row-tool,
.tv-row-action {
  font-weight: 600;
}
.tv-row-tool {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}
.tv-row-target {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  opacity: 0.8;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 60%;
}
.tv-row-dim {
  opacity: 0.5;
  font-size: 11px;
}
.tv-row-time {
  margin-left: auto;
  opacity: 0.4;
  font-size: 11px;
  font-variant-numeric: tabular-nums;
}
.tv-toggle {
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.5;
  padding: 0;
  display: flex;
}
.tv-toggle-open {
  transform: rotate(90deg);
}
.tv-row-detail {
  margin: 2px 0 0;
  opacity: 0.7;
  line-height: 1.4;
}
.tv-json {
  margin: 6px 0 2px;
  padding: 8px 10px;
  border-radius: 6px;
  background: rgba(15, 23, 42, 0.6);
  font-size: 11px;
  line-height: 1.45;
  overflow-x: auto;
  white-space: pre;
}
</style>
