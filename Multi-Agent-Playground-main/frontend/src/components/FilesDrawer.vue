<script setup>
import { computed, ref, watch } from "vue";
import { File, Folder, FolderOpen, RefreshCw, X } from "lucide-vue-next";
import { fetchWorkspaceFile, fetchWorkspaceTree } from "../api";

const props = defineProps({
  open: { type: Boolean, default: false },
  // File paths this run generated (from the trace); may include directories.
  traceFiles: { type: Array, default: () => [] },
});
const emit = defineEmits(["close"]);

const tab = ref("run"); // "run" | "browse"
const dirEntries = ref([]);
const dirPath = ref("");
const dirLoading = ref(false);
const dirError = ref("");

const selectedPath = ref("");
const fileContent = ref("");
const fileTruncated = ref(false);
const fileLoading = ref(false);
const fileError = ref("");

const runFiles = computed(() => {
  const seen = new Set();
  const out = [];
  for (const raw of props.traceFiles) {
    const p = String(raw || "").trim();
    if (!p || seen.has(p)) continue;
    seen.add(p);
    out.push(p);
  }
  return out;
});

function baseName(path) {
  const parts = String(path).split("/").filter(Boolean);
  return parts[parts.length - 1] || path;
}

async function loadDir(path = "") {
  dirLoading.value = true;
  dirError.value = "";
  try {
    const data = await fetchWorkspaceTree(path);
    dirPath.value = data.path === "." ? "" : data.path;
    dirEntries.value = data.entries || [];
  } catch (error) {
    dirError.value = error?.message || "Could not list directory.";
    dirEntries.value = [];
  } finally {
    dirLoading.value = false;
  }
}

async function openFile(path) {
  selectedPath.value = path;
  fileLoading.value = true;
  fileError.value = "";
  fileContent.value = "";
  fileTruncated.value = false;
  try {
    const data = await fetchWorkspaceFile(path);
    fileContent.value = data.content ?? "";
    fileTruncated.value = Boolean(data.truncated);
  } catch (error) {
    fileError.value = error?.message || "Could not read file.";
  } finally {
    fileLoading.value = false;
  }
}

function parentDir() {
  const parts = dirPath.value.split("/").filter(Boolean);
  parts.pop();
  loadDir(parts.join("/"));
}

watch(
  () => props.open,
  (isOpen) => {
    if (!isOpen) return;
    tab.value = runFiles.value.length ? "run" : "browse";
    if (tab.value === "browse" && !dirEntries.value.length) loadDir("");
  },
);

watch(tab, (value) => {
  if (value === "browse" && !dirEntries.value.length && !dirLoading.value) loadDir("");
});
</script>

<template>
  <div v-if="open" class="files-drawer-overlay" @click.self="emit('close')">
    <aside class="files-drawer glass-panel">
      <header class="files-drawer-head">
        <div class="files-drawer-tabs">
          <button type="button" :class="{ active: tab === 'run' }" @click="tab = 'run'">
            This run ({{ runFiles.length }})
          </button>
          <button type="button" :class="{ active: tab === 'browse' }" @click="tab = 'browse'">
            Browse workspace
          </button>
        </div>
        <button type="button" class="files-drawer-close" aria-label="Close" @click="emit('close')">
          <X :size="16" />
        </button>
      </header>

      <div class="files-drawer-body">
        <div class="files-drawer-list">
          <!-- This run -->
          <template v-if="tab === 'run'">
            <p v-if="!runFiles.length" class="files-drawer-empty">
              No files generated in this run yet.
            </p>
            <button
              v-for="path in runFiles"
              :key="path"
              type="button"
              class="files-drawer-entry"
              :class="{ active: selectedPath === path }"
              @click="openFile(path)"
            >
              <File :size="14" />
              <span class="files-drawer-entry-name">{{ path }}</span>
            </button>
          </template>

          <!-- Browse -->
          <template v-else>
            <div class="files-drawer-crumbs">
              <button type="button" @click="loadDir('')">workspace</button>
              <span v-if="dirPath">/ {{ dirPath }}</span>
              <button
                v-if="dirPath"
                type="button"
                class="files-drawer-up"
                @click="parentDir"
              >
                up
              </button>
              <button type="button" class="files-drawer-up" @click="loadDir(dirPath)">
                <RefreshCw :size="12" />
              </button>
            </div>
            <p v-if="dirLoading" class="files-drawer-empty">Loading…</p>
            <p v-else-if="dirError" class="files-drawer-empty error">{{ dirError }}</p>
            <template v-else>
              <button
                v-for="entry in dirEntries"
                :key="entry.path"
                type="button"
                class="files-drawer-entry"
                :class="{ active: selectedPath === entry.path }"
                @click="entry.is_dir ? loadDir(entry.path) : openFile(entry.path)"
              >
                <component :is="entry.is_dir ? Folder : File" :size="14" />
                <span class="files-drawer-entry-name">{{ entry.name }}</span>
                <span v-if="!entry.is_dir && entry.size != null" class="files-drawer-entry-size">
                  {{ entry.size }} B
                </span>
              </button>
            </template>
          </template>
        </div>

        <div class="files-drawer-preview">
          <header v-if="selectedPath" class="files-drawer-preview-head">
            <FolderOpen :size="14" />
            <span>{{ selectedPath }}</span>
            <span v-if="fileTruncated" class="files-drawer-trunc">truncated</span>
          </header>
          <p v-if="!selectedPath" class="files-drawer-empty">Select a file to preview.</p>
          <p v-else-if="fileLoading" class="files-drawer-empty">Loading…</p>
          <p v-else-if="fileError" class="files-drawer-empty error">{{ fileError }}</p>
          <pre v-else class="files-drawer-code">{{ fileContent }}</pre>
        </div>
      </div>
    </aside>
  </div>
</template>

<style scoped>
.files-drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(2, 6, 23, 0.45);
  display: flex;
  justify-content: flex-end;
  z-index: 60;
}
.files-drawer {
  width: min(880px, 92vw);
  height: 100%;
  display: flex;
  flex-direction: column;
  border-radius: 0;
  padding: 0;
}
.files-drawer-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}
.files-drawer-tabs {
  display: flex;
  gap: 6px;
}
.files-drawer-tabs button {
  padding: 5px 10px;
  font-size: 12px;
  border-radius: 8px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  background: transparent;
  color: inherit;
  cursor: pointer;
}
.files-drawer-tabs button.active {
  background: rgba(59, 130, 246, 0.18);
  border-color: rgba(59, 130, 246, 0.5);
}
.files-drawer-close {
  background: transparent;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.7;
}
.files-drawer-body {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 280px 1fr;
}
.files-drawer-list {
  border-right: 1px solid rgba(148, 163, 184, 0.2);
  overflow-y: auto;
  padding: 8px;
}
.files-drawer-entry {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 8px;
  font-size: 12px;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-align: left;
}
.files-drawer-entry:hover {
  background: rgba(148, 163, 184, 0.12);
}
.files-drawer-entry.active {
  background: rgba(59, 130, 246, 0.16);
}
.files-drawer-entry-name {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.files-drawer-entry-size {
  opacity: 0.5;
  font-size: 11px;
}
.files-drawer-crumbs {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  opacity: 0.8;
  padding: 4px 6px 8px;
  flex-wrap: wrap;
}
.files-drawer-crumbs button {
  background: transparent;
  border: 1px solid rgba(148, 163, 184, 0.25);
  border-radius: 6px;
  color: inherit;
  cursor: pointer;
  padding: 2px 6px;
}
.files-drawer-preview {
  overflow: auto;
  padding: 10px 12px;
  min-width: 0;
}
.files-drawer-preview-head {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  opacity: 0.85;
  margin-bottom: 8px;
  word-break: break-all;
}
.files-drawer-trunc {
  font-size: 10px;
  padding: 1px 5px;
  border-radius: 6px;
  background: rgba(234, 179, 8, 0.2);
}
.files-drawer-code {
  margin: 0;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre;
  overflow-x: auto;
}
.files-drawer-empty {
  font-size: 12px;
  opacity: 0.6;
  padding: 10px 6px;
}
.files-drawer-empty.error {
  color: #f87171;
  opacity: 0.95;
}
</style>
