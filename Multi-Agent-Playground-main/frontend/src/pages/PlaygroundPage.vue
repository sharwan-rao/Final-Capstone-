<script setup>
import { computed, inject, ref } from "vue";
import { FolderTree } from "lucide-vue-next";
import ChatRunner from "../components/ChatRunner.vue";
import FilesDrawer from "../components/FilesDrawer.vue";
import GraphViewer from "../components/GraphViewer.vue";
import TraceViewer from "../components/TraceViewer.vue";
import { I18N_KEY } from "../i18n";

const props = defineProps({
  workflows: {
    type: Array,
    required: true,
  },
  agents: {
    type: Array,
    required: true,
  },
  selectedWorkflowId: {
    type: String,
    default: "",
  },
  selectedWorkflow: {
    type: Object,
    default: null,
  },
  selectedGraph: {
    type: Object,
    default: null,
  },
  activeNodeId: {
    type: String,
    default: "",
  },
  loading: {
    type: Boolean,
    default: false,
  },
  trace: {
    type: Array,
    default: () => [],
  },
  tracePlaying: {
    type: Boolean,
    default: false,
  },
  chatMessages: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["run", "clear", "stop", "select-workflow"]);

const i18n = inject(I18N_KEY, null);
const t = i18n?.t || ((key) => key);
const workflowTypeLabel = i18n?.workflowTypeLabel || ((type) => type);
const leftVisible = ref(true);
const rightVisible = ref(true);
const filesOpen = ref(false);

const traceFiles = computed(() => {
  const out = [];
  for (const event of props.trace || []) {
    const files = event?.payload?.generated_files;
    if (Array.isArray(files)) out.push(...files);
  }
  return out;
});
const traceFileCount = computed(() => new Set(traceFiles.value).size);
</script>

<template>
  <div class="playground-shell">
    <div
      class="playground-grid"
      :class="{
        'left-collapsed': !leftVisible,
        'right-collapsed': !rightVisible,
      }"
    >
    <aside v-if="leftVisible" class="playground-col-left">
      <section class="glass-panel workflow-select-card">
        <label class="field-label">{{ t("workflow.selectWorkflow") }}</label>
        <select
          class="workflow-native-select"
          :value="props.selectedWorkflowId"
          @change="$emit('select-workflow', $event.target.value)"
        >
          <option v-for="workflow in props.workflows" :key="workflow.id" :value="workflow.id">
            {{ workflow.name }} - {{ workflowTypeLabel(workflow.type) }}
          </option>
        </select>
      </section>

      <GraphViewer
        :graph="props.selectedGraph"
        :active-node-id="props.activeNodeId"
        :trace="props.trace"
      />
    </aside>

    <section class="playground-col-center">
      <ChatRunner
        :selected-workflow-id="props.selectedWorkflowId"
        :selected-workflow="props.selectedWorkflow"
        :loading="props.loading"
        :left-visible="leftVisible"
        :right-visible="rightVisible"
        :messages="props.chatMessages"
        @run="$emit('run', $event)"
        @clear="$emit('clear')"
        @stop="$emit('stop')"
        @toggle-left="leftVisible = !leftVisible"
        @toggle-right="rightVisible = !rightVisible"
      />
    </section>

    <aside v-if="rightVisible" class="playground-col-right">
      <TraceViewer :trace="props.trace" :playing="props.tracePlaying" />
    </aside>
    </div>

    <button type="button" class="playground-files-fab" @click="filesOpen = true">
      <FolderTree :size="16" />
      Files<span v-if="traceFileCount"> ({{ traceFileCount }})</span>
    </button>

    <FilesDrawer :open="filesOpen" :trace-files="traceFiles" @close="filesOpen = false" />
  </div>
</template>

<style scoped>
.playground-files-fab {
  position: absolute;
  right: 18px;
  bottom: 18px;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  font-size: 13px;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: rgba(15, 23, 42, 0.9);
  color: #e2e8f0;
  cursor: pointer;
  box-shadow: 0 8px 24px rgba(2, 6, 23, 0.35);
  z-index: 40;
}
.playground-files-fab:hover {
  border-color: rgba(59, 130, 246, 0.6);
}
</style>
