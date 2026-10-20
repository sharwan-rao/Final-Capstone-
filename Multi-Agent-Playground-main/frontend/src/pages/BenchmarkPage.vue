<script setup>
import { computed, ref, watch } from "vue";
import {
  BarChart3,
  Calculator,
  CheckCircle2,
  Clock3,
  Eye,
  EyeOff,
  GitBranch,
  ListChecks,
  MessageSquare,
  Play,
  Repeat,
  Shuffle,
  Sparkles,
  XCircle,
} from "lucide-vue-next";
import { marked } from "marked";

const props = defineProps({
  workflows: { type: Array, required: true },
  selectedWorkflowId: { type: String, default: "" },
  result: { type: Object, default: null },
  loading: { type: Boolean, default: false },
});

const emit = defineEmits(["run", "inspect"]);
const prompt = ref("Calculate the exact compound interest on a $15,000 investment at 6.5% annual interest compounded monthly for 8 years. Show each intermediate step and calculation formula clearly.");
const selectedIds = ref([]);
const expandedResponseId = ref("");

function toggleResponse(workflowId) {
  expandedResponseId.value = expandedResponseId.value === workflowId ? "" : workflowId;
}

function renderMarkdown(content) {
  return marked.parse(String(content || ""));
}

const demoPresets = [
  {
    id: "math",
    title: "Math & Logic",
    tag: "Router Specialist",
    icon: Calculator,
    prompt: "Calculate the exact compound interest on a $15,000 investment at 6.5% annual interest compounded monthly for 8 years. Show each intermediate step and calculation formula clearly.",
    desc: "Directs straight to Data & Logic Expert for precision calculation.",
  },
  {
    id: "planner",
    title: "Multi-Step Brief",
    tag: "Planner Executor",
    icon: ListChecks,
    prompt: "Analyze the current energy consumption of AI data centers, calculate the projected power demand through 2030, and write an executive briefing with 3 actionable recommendations for sustainable computing.",
    desc: "Decomposes into 3 subtasks across research, math, and writing before synthesizing.",
  },
  {
    id: "supervisor",
    title: "Code & Security Guide",
    tag: "Supervisor Dynamic",
    icon: Repeat,
    prompt: "Design a Python security auditing script for REST API endpoints with rate-limiting validation, test it with edge cases, and produce a polished implementation guide.",
    desc: "Supervisor coordinates code writing, testing verification, and doc formatting.",
  },
  {
    id: "handoff",
    title: "RSA Cryptography",
    tag: "Peer Handoff",
    icon: Shuffle,
    prompt: "Analyze the historical origins of cryptography, formulate a mathematical explanation of RSA public-key encryption, and craft an intuitive analogy explaining it to non-technical readers.",
    desc: "Passes context smoothly: Research Analyst -> Data & Logic -> Creative Writer.",
  },
];

watch(
  () => [props.workflows, props.selectedWorkflowId],
  () => {
    if (selectedIds.value.length) return;
    const preferred = props.workflows.find((workflow) => workflow.id === props.selectedWorkflowId)
      || props.workflows[0];
    if (preferred) selectedIds.value = [preferred.id];
  },
  { immediate: true, deep: true },
);

const selectedCount = computed(() => selectedIds.value.length);
const completed = computed(() => (props.result?.results || []).filter((item) => item.status === "completed"));
const fastestId = computed(() => {
  const sorted = [...completed.value].sort((a, b) => a.metrics.duration_ms - b.metrics.duration_ms);
  return sorted[0]?.workflow_id || "";
});

function toggleWorkflow(workflowId) {
  if (selectedIds.value.includes(workflowId)) {
    selectedIds.value = selectedIds.value.filter((id) => id !== workflowId);
    return;
  }
  selectedIds.value = [...selectedIds.value, workflowId];
}

function selectAllWorkflows() {
  if (selectedIds.value.length === props.workflows.length) {
    selectedIds.value = [];
  } else {
    selectedIds.value = props.workflows.map((w) => w.id);
  }
}

function run() {
  const userInput = prompt.value.trim();
  if (!userInput || !selectedIds.value.length || props.loading) return;
  emit("run", { workflow_ids: selectedIds.value, user_input: userInput });
}

function formatDuration(durationMs) {
  if (durationMs < 1000) return `${durationMs} ms`;
  return `${(durationMs / 1000).toFixed(2)} s`;
}
</script>

<template>
  <div class="benchmark-page page-stack">
    <section class="glass-panel benchmark-hero">
      <div>
        <span class="chip chip-blue"><BarChart3 :size="14" /> Experiment mode</span>
        <h2>Workflow Benchmark & Comparison</h2>
        <p>Send identical prompts through multiple workflows simultaneously to compare execution steps, speed, and routing accuracy.</p>
      </div>
      <div class="benchmark-summary">
        <strong>{{ selectedCount }}</strong>
        <span>Selected</span>
      </div>
    </section>

    <section class="benchmark-grid">
      <article class="glass-panel benchmark-setup">
        <div class="section-header compact">
          <div class="workflow-header-row">
            <div>
              <h3><GitBranch :size="18" class="text-blue-600" /> Select Workflows to Compare</h3>
              <p>Each workflow receives the exact same prompt in a clean session without prior history.</p>
            </div>
            <button type="button" class="select-all-btn" @click="selectAllWorkflows">
              {{ selectedIds.length === workflows.length ? 'Deselect all' : 'Select all' }}
            </button>
          </div>
        </div>

        <div class="benchmark-workflows">
          <button
            v-for="workflow in workflows"
            :key="workflow.id"
            type="button"
            class="benchmark-workflow"
            :class="{ selected: selectedIds.includes(workflow.id) }"
            @click="toggleWorkflow(workflow.id)"
          >
            <span class="benchmark-checkbox">{{ selectedIds.includes(workflow.id) ? '✓' : '' }}</span>
            <span>
              <strong>{{ workflow.name }}</strong>
              <small>{{ workflow.type.replace(/_/g, ' ') }}</small>
            </span>
          </button>
        </div>

        <!-- Preset Prompts for Demos -->
        <div class="benchmark-presets">
          <div class="preset-header">
            <span class="preset-title"><Sparkles :size="14" class="text-amber-500" /> Click a Demo Preset Prompt:</span>
            <span class="preset-hint">Shows how different workflows alter the outcome</span>
          </div>
          <div class="preset-chips">
            <button
              v-for="item in demoPresets"
              :key="item.id"
              type="button"
              class="preset-chip"
              :class="{ active: prompt === item.prompt }"
              @click="prompt = item.prompt"
              :title="item.desc"
            >
              <component :is="item.icon" :size="13" />
              <span>{{ item.title }}</span>
              <span class="preset-badge">{{ item.tag }}</span>
            </button>
          </div>
        </div>

        <label class="field-label" for="benchmark-prompt">Shared Benchmark Prompt</label>
        <textarea id="benchmark-prompt" v-model="prompt" class="benchmark-prompt" rows="5" :disabled="loading" placeholder="Type or select a benchmark prompt..." />

        <button type="button" class="primary-button benchmark-run" :disabled="!selectedCount || !prompt.trim() || loading" @click="run">
          <Play :size="16" />
          {{ loading ? 'Running comparison…' : `Run ${selectedCount || ''} workflow${selectedCount === 1 ? '' : 's'} comparison` }}
        </button>
      </article>

      <article class="glass-panel benchmark-guide">
        <h3>What is measured</h3>
        <dl>
          <div><dt>Duration</dt><dd>End-to-end execution latency in seconds</dd></div>
          <div><dt>Trace events</dt><dd>Full chain of runtime routing decisions</dd></div>
          <div><dt>Agent steps</dt><dd>Specialist agents invoked to produce the answer</dd></div>
          <div><dt>Handoffs</dt><dd>Transitions between supervisor, planner, or peer agents</dd></div>
        </dl>
        <div class="benchmark-note">
          <strong>💡 Demo Tip:</strong>
          Run all workflows on a multi-intent prompt (like <em>Multi-Step Brief</em>) to demonstrate how Planner Executor partitions tasks cleanly compared to Single Agent Chat!
        </div>
      </article>
    </section>

    <section v-if="result" class="glass-panel benchmark-results">
      <div class="section-header">
        <div>
          <h3><BarChart3 :size="20" class="text-blue-600" /> Benchmark Results</h3>
          <p>{{ completed.length }} of {{ result.results.length }} workflows completed for this prompt.</p>
        </div>
      </div>

      <div class="benchmark-table-wrap">
        <table class="benchmark-table">
          <thead>
            <tr>
              <th>Workflow</th>
              <th>Status</th>
              <th>Duration</th>
              <th>Trace Events</th>
              <th>Nodes Visited</th>
              <th>Agent Steps</th>
              <th>Handoffs</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in result.results" :key="item.workflow_id" :class="{ fastest: item.workflow_id === fastestId }">
              <td>
                <strong>{{ item.workflow_name }}</strong>
                <small>{{ item.workflow_type.replace(/_/g, ' ') }}</small>
              </td>
              <td>
                <span v-if="item.status === 'completed'" class="benchmark-status success"><CheckCircle2 :size="15" /> Complete</span>
                <span v-else class="benchmark-status failed"><XCircle :size="15" /> Failed</span>
              </td>
              <td><Clock3 :size="14" /> {{ formatDuration(item.metrics.duration_ms) }}</td>
              <td>{{ item.metrics.trace_events }}</td>
              <td>{{ item.metrics.nodes_visited }}</td>
              <td>{{ item.metrics.agent_steps }}</td>
              <td>{{ item.metrics.handoffs }}</td>
              <td>
                <div class="benchmark-action-group">
                  <button
                    v-if="item.status === 'completed'"
                    type="button"
                    class="action-btn action-btn-blue"
                    @click="$emit('inspect', { ...item, user_input: result?.user_input || prompt })"
                    title="Open in Playground with chat history and live graph"
                  >
                    <GitBranch :size="13" /> Open graph
                  </button>
                  <button
                    v-if="item.status === 'completed' && item.assistant_message"
                    type="button"
                    class="action-btn action-btn-subtle"
                    @click="toggleResponse(item.workflow_id)"
                    title="Quick preview response text"
                  >
                    <component :is="expandedResponseId === item.workflow_id ? EyeOff : Eye" :size="13" />
                    {{ expandedResponseId === item.workflow_id ? 'Hide answer' : 'View answer' }}
                  </button>
                  <span v-else-if="item.status === 'failed'" class="benchmark-error" :title="item.error">{{ item.error || 'Run failed' }}</span>
                </div>
              </td>
            </tr>

            <!-- Expandable Response Row -->
            <tr v-if="expandedResponseId === item.workflow_id && item.assistant_message" class="benchmark-response-row">
              <td colspan="8">
                <div class="benchmark-response-card">
                  <div class="benchmark-response-header">
                    <div class="response-title">
                      <MessageSquare :size="15" class="text-blue-600" />
                      <strong>Response from {{ item.workflow_name }}</strong>
                      <span class="response-badge">{{ item.workflow_type.replace(/_/g, ' ') }}</span>
                    </div>
                    <button
                      type="button"
                      class="action-btn action-btn-blue text-xs"
                      @click="$emit('inspect', { ...item, user_input: result?.user_input || prompt })"
                    >
                      <GitBranch :size="12" /> Open in Playground Chat &amp; Graph &rarr;
                    </button>
                  </div>
                  <div class="benchmark-response-body markdown-body" v-html="renderMarkdown(item.assistant_message)"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>
  </div>
</template>

<style scoped>
.benchmark-hero, .benchmark-grid {
  display: grid;
  gap: 20px;
}
.benchmark-hero {
  grid-template-columns: 1fr auto;
  align-items: center;
  padding: 28px 32px;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.98), rgba(241, 245, 249, 0.92));
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 20px;
}
.benchmark-hero h2 {
  margin: 10px 0 6px;
  font-size: 28px;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.02em;
}
.benchmark-hero p {
  margin: 0;
  color: #475569;
  font-size: 15px;
}
.benchmark-summary {
  display: grid;
  place-items: center;
  width: 96px;
  height: 96px;
  border-radius: 24px;
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: #ffffff;
  box-shadow: 0 10px 24px rgba(37, 99, 235, 0.28);
}
.benchmark-summary strong {
  font-size: 32px;
  font-weight: 800;
  line-height: 1;
  color: #ffffff;
}
.benchmark-summary span {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: rgba(255, 255, 255, 0.9);
}

.benchmark-grid {
  grid-template-columns: minmax(0, 1.75fr) minmax(280px, 0.85fr);
}
.benchmark-setup, .benchmark-guide, .benchmark-results {
  padding: 24px 28px;
  background: #ffffff;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(15, 23, 42, 0.05);
}

.workflow-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  width: 100%;
}
.select-all-btn {
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}
.select-all-btn:hover {
  background: #2563eb;
  color: #ffffff;
}

.section-header h3 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 6px;
  font-size: 19px;
  font-weight: 800;
  color: #0f172a;
}
.section-header p {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.benchmark-workflows {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
  gap: 12px;
  margin: 16px 0 20px;
}
.benchmark-workflow {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  text-align: left;
  color: #0f172a;
  border: 1.5px solid #cbd5e1;
  background: #ffffff;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
}
.benchmark-workflow:hover {
  border-color: #93c5fd;
  transform: translateY(-1.5px);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.08);
}
.benchmark-workflow strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}
.benchmark-workflow small {
  display: block;
  margin-top: 3px;
  color: #64748b;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}
.benchmark-workflow.selected {
  border-color: #2563eb;
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.95), rgba(219, 234, 254, 0.6));
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.15);
}
.benchmark-workflow.selected strong {
  color: #1d4ed8;
}
.benchmark-workflow.selected small {
  color: #2563eb;
}
.benchmark-checkbox {
  display: grid;
  place-items: center;
  width: 22px;
  height: 22px;
  border-radius: 6px;
  border: 2px solid #94a3b8;
  background: #f8fafc;
  color: transparent;
  font-weight: 800;
  font-size: 13px;
  transition: all 0.15s ease;
  flex-shrink: 0;
}
.benchmark-workflow.selected .benchmark-checkbox {
  background: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
}

.benchmark-presets {
  margin-bottom: 18px;
  padding: 14px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}
.preset-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
  gap: 8px;
}
.preset-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 700;
  color: #0f172a;
}
.preset-hint {
  font-size: 12px;
  color: #64748b;
}
.preset-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.preset-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 12px;
  background: #ffffff;
  border: 1.5px solid #cbd5e1;
  border-radius: 10px;
  color: #1e293b;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}
.preset-chip:hover {
  border-color: #2563eb;
  color: #1d4ed8;
  background: #eff6ff;
  transform: translateY(-1px);
}
.preset-chip.active {
  background: #2563eb;
  border-color: #2563eb;
  color: #ffffff;
  box-shadow: 0 3px 10px rgba(37, 99, 235, 0.25);
}
.preset-badge {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 999px;
  background: rgba(148, 163, 184, 0.18);
  color: #475569;
  font-weight: 600;
}
.preset-chip.active .preset-badge {
  background: rgba(255, 255, 255, 0.25);
  color: #ffffff;
}

.field-label {
  display: block;
  font-size: 13px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 6px;
}

.benchmark-prompt {
  width: 100%;
  box-sizing: border-box;
  resize: vertical;
  margin: 4px 0 16px;
  padding: 14px 16px;
  border: 1.5px solid #cbd5e1;
  border-radius: 12px;
  color: #0f172a;
  background: #f8fafc;
  font-size: 14px;
  line-height: 1.6;
  font-family: inherit;
  transition: all 0.2s ease;
}
.benchmark-prompt:focus {
  outline: none;
  border-color: #2563eb;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.12);
}

.benchmark-run {
  width: 100%;
  justify-content: center;
  padding: 13px 20px;
  font-size: 15px;
  font-weight: 700;
  border-radius: 12px;
}

.benchmark-guide h3 {
  margin-top: 0;
  font-size: 18px;
  font-weight: 800;
  color: #0f172a;
}
.benchmark-guide dl {
  margin: 18px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.benchmark-guide dl div {
  padding: 12px 14px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  transition: border-color 0.15s ease;
}
.benchmark-guide dl div:hover {
  border-color: #cbd5e1;
}
.benchmark-guide dt {
  color: #1e40af;
  font-size: 14px;
  font-weight: 700;
}
.benchmark-guide dd {
  margin: 3px 0 0;
  color: #475569;
  font-size: 13px;
  line-height: 1.4;
}
.benchmark-note {
  margin-top: 16px;
  color: #1d4ed8;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 14px 16px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
}
.benchmark-note strong {
  display: block;
  margin-bottom: 4px;
  color: #1e40af;
}

.benchmark-results {
  margin-top: 24px;
}
.benchmark-table-wrap {
  overflow-x: auto;
  margin-top: 16px;
  border: 1px solid #cbd5e1;
  border-radius: 14px;
}
.benchmark-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
  background: #ffffff;
}
.benchmark-table th {
  padding: 12px 16px;
  color: #334155;
  background: #f1f5f9;
  font-size: 12px;
  font-weight: 700;
  text-align: left;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid #cbd5e1;
}
.benchmark-table td {
  padding: 14px 16px;
  border-top: 1px solid #e2e8f0;
  color: #1e293b;
  font-size: 14px;
  font-weight: 500;
}
.benchmark-table tr:hover {
  background: #f8fafc;
}
.benchmark-table td:first-child strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}
.benchmark-table td:first-child small {
  display: block;
  margin-top: 3px;
  color: #64748b;
  font-size: 12px;
  font-weight: 500;
  text-transform: capitalize;
}
.benchmark-table tr.fastest {
  background: #ecfdf5;
}
.benchmark-table tr.fastest td {
  color: #065f46;
  font-weight: 600;
}
.benchmark-table td:nth-child(3) {
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  font-weight: 600;
}
.benchmark-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
}
.benchmark-status.success {
  color: #059669;
}
.benchmark-status.failed {
  color: #dc2626;
}
.benchmark-error {
  display: block;
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #dc2626;
  font-size: 12px;
}
.text-button {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}
.text-button:hover {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}

.benchmark-action-group {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.action-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 6px 11px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.action-btn-blue {
  color: #2563eb;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
}
.action-btn-blue:hover {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
}
.action-btn-subtle {
  color: #475569;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
}
.action-btn-subtle:hover {
  background: #e2e8f0;
  color: #0f172a;
}
.benchmark-response-row {
  background: #f8fafc;
}
.benchmark-response-row td {
  padding: 0 16px 16px !important;
  border-top: none !important;
}
.benchmark-response-card {
  background: #ffffff;
  border: 1.5px solid #bfdbfe;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08);
}
.benchmark-response-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 16px;
  background: #eff6ff;
  border-bottom: 1px solid #dbeafe;
}
.response-title {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1e3a8a;
  font-size: 13px;
}
.response-badge {
  font-size: 11px;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(37, 99, 235, 0.12);
  color: #2563eb;
  font-weight: 600;
  text-transform: capitalize;
}
.benchmark-response-body {
  padding: 16px;
  font-size: 14px;
  line-height: 1.6;
  color: #0f172a;
  max-height: 380px;
  overflow-y: auto;
}

@media (max-width: 800px) {
  .benchmark-grid { grid-template-columns: 1fr; }
  .benchmark-hero { grid-template-columns: 1fr; }
  .benchmark-summary { display: none; }
}
</style>

