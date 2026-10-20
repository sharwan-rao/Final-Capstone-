import { computed, ref } from "vue";

export const I18N_KEY = Symbol("ui-i18n");

const messages = {
  "en-US": {
    nav: {
      overview: "Overview",
      agents: "Agents",
      workflows: "Orchestration",
      playground: "Run",
      settings: "Settings",
    },
    brand: {
      subtitle: "Multi-agent orchestration and trace system",
    },
    status: {
      ready: "System Ready",
    },

    page: {
      agentsTitle: "Agents",
      agentsDesc: "Create role specialists for reuse across different orchestrations.",
      workflowsTitle: "Orchestration",
      workflowsDesc: "Define collaboration patterns and create executable setups.",
    },
    settings: {
      title: "Settings",
      desc: "Configure model access for the desktop app runtime.",
      modelProfiles: "Model Profiles",
      modelProfilesDesc: "Create multiple model configurations. Save changes inside each profile editor.",
      addProfile: "Add Profile",
      active: "Active",
      setActive: "Set Active",
      editProfile: "Edit Profile",
      closeEditor: "Close",
      profileName: "Profile Name",
      profileNamePlaceholder: "Profile name",
      providerPreset: "Provider Preset",
      apiKey: "OpenAI API Key",
      apiKeyPlaceholder: "sk-...",
      baseUrl: "Base URL",
      baseUrlPlaceholder: "https://api.openai.com/v1",
      model: "Model",
      modelPlaceholder: "gpt-4o-mini",
      envVars: "Environment Variables",
      envVarsDesc: "Add any extra env vars required by tools or providers.",
      envVarsHint: "Press Enter or click save on a row to persist environment variables.",
      addEnvVar: "Add Variable",
      envKeyPlaceholder: "TAVILY_API_KEY",
      envValuePlaceholder: "value",
      saveProfile: "Save Profile",
      saveEnvVar: "Save",
      envNoValue: "No value",
      envEmpty: "No extra environment variables configured.",
      storageLabel: "Env File",
      save: "Save Settings",
      saving: "Saving...",
    },
    overview: {
      chip: "Orchestration-first Playground",
      headline1: "Define pattern first.",
      headline2: "Observe agents in motion.",
      desc: "This UI demonstrates agents, orchestration routing, and runtime trace in one clear experience.",
      flowTitle: "Flow",
      flowDesc: "Follow this order for the clearest walkthrough.",
      step1Title: "Create Agents",
      step1Desc: "Define reusable specialists.",
      step2Title: "Define Pattern",
      step2Desc: "Select a collaboration pattern and create a setup.",
      step3Title: "Run Playground",
      step3Desc: "Send messages and inspect graph plus trace.",
      agents: "Agents",
      workflows: "Setups",
      templates: "Patterns",
    },
    agent: {
      registryTitle: "Agent Registry",
      registryDesc: "Create and reuse specialists across orchestrations.",
      new: "New Agent",
      name: "Agent name",
      role: "Role description",
      prompt: "System prompt",
      save: "Save",
      cancel: "Cancel",
      systemPrompt: "System prompt",
    },
    workflow: {
      catalogTitle: "Orchestration Catalog",
      catalogDesc: "Choose a collaboration pattern and create executable setups.",
      new: "New Setup",
      setup: "Setup Configuration",
      name: "Setup name",
      enableFinalizer: "Enable Finalizer",
      bindAgents: "Bind Agents",
      requiresAtLeast: "This pattern requires at least {count} agents.",
      save: "Save Setup",
      cancel: "Cancel",
      selected: "selected",
      current: "Current setup",
      specialists: "Agents",
      finalizer: "Finalizer",
      on: "On",
      off: "Off",
      selectWorkflow: "Select Setup",
      template_router_specialists: "Router Specialists",
      template_planner_executor: "Planner Executor",
      template_supervisor_dynamic: "Supervisor Dynamic",
      template_single_agent_chat: "Single Agent Chat",
      template_peer_handoff: "Peer Handoff",
      template_desc_router_specialists:
        "Router selects the best specialist for the user intent, then optionally passes through a finalizer.",
      template_desc_planner_executor:
        "Planner decomposes the request into sub-tasks, delegates each task to workers, then synthesizes a final answer.",
      template_desc_supervisor_dynamic:
        "Supervisor decides delegation at runtime, loops through workers as needed, and composes the final answer.",
      template_desc_single_agent_chat:
        "Direct chat with one selected agent using a minimal start -> agent -> end graph.",
      template_desc_peer_handoff:
        "Router selects the first owner, then specialists hand work to each other inside a shared collaboration zone.",
    },
    chat: {
      title: "Run",
      active: "Active setup",
      noneSelected: "No setup selected",
      clear: "Clear",
      presets: "Example Scenarios",
      fill: "Fill",
      presetRouter: "Single intent routing",
      presetPlanner: "Structured multi-part task",
      presetSupervisor: "Dynamic delegation with risks",
      startRun: "Start a run",
      startRunDesc: "Send a prompt and watch routing, graph highlights and trace updates.",
      thinking: "Thinking...",
      inputPlaceholder: "Type a test prompt...",
      send: "Send",
      assistant: "Assistant",
    },
    graph: {
      title: "Graph",
      subtitle: "Runtime highlighted nodes",
      liveGraph: "Live Graph",
      empty: "Select a setup to display its graph.",
      activeNode: "Active node",
      waiting: "Waiting for interaction...",
      live: "Live",
    },
    trace: {
      title: "Trace",
      subtitle: "Runtime events and routing decisions",
      live: "Live",
      playing: "Playing",
      showAll: "All events",
      showKey: "Key only",
      empty: "Run a setup to view events here.",
      payload: "payload",
    },
  },
};

function getByPath(obj, path) {
  return path.split(".").reduce((current, key) => current?.[key], obj);
}

function interpolate(text, vars = {}) {
  return String(text).replace(/\{(\w+)\}/g, (_, key) => vars[key] ?? `{${key}}`);
}

export function createUiI18n() {
  const locale = ref("en-US");
  const dict = computed(() => messages["en-US"]);

  function setLocale(_nextLocale) {
    // English only — language switching is disabled
  }

  function t(path, vars = {}) {
    const found = getByPath(dict.value, path);
    if (typeof found === "string") return interpolate(found, vars);
    return path;
  }

  function workflowTypeLabel(type) {
    const path = `workflow.template_${type}`;
    const value = t(path);
    if (value !== path) return value;

    const fallbackLabels = {
      router_specialists: "Router Specialists",
      planner_executor: "Planner Executor",
      supervisor_dynamic: "Supervisor Dynamic",
      single_agent_chat: "Single Agent Chat",
      peer_handoff: "Peer Handoff",
    };
    return fallbackLabels[type] || type;
  }

  function workflowTypeDesc(type, fallback = "") {
    const value = t(`workflow.template_desc_${type}`);
    if (value !== `workflow.template_desc_${type}`) return value;
    const fallbackDescriptions = {
      router_specialists:
        "Router selects the best specialist for the user intent, then optionally passes through a finalizer.",
      planner_executor:
        "Planner decomposes the request into sub-tasks, delegates each task to workers, then synthesizes a final answer.",
      supervisor_dynamic:
        "Supervisor decides delegation at runtime, loops through workers as needed, and composes the final answer.",
      single_agent_chat:
        "Direct chat with one selected agent using a minimal start -> agent -> end graph.",
      peer_handoff:
        "Router selects the first owner, then specialists hand work to each other inside a shared collaboration zone.",
    };
    return fallbackDescriptions[type] || fallback;
  }

  return {
    locale,
    setLocale,
    t,
    workflowTypeLabel,
    workflowTypeDesc,
  };
}
