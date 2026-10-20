# Multi-Agent Playground

![](https://jyunpan.oss-cn-beijing.aliyuncs.com/github/0.png)
![](https://jyunpan.oss-cn-beijing.aliyuncs.com/github/1.png)


## Project Structure

```
Multi-Agent-Playground/
├── backend/          # Python FastAPI backend
│   ├── app/         # Application source code
│   │   └── workflows/  # 5 workflow implementations built on LangGraph
│   ├── skills/      # Installed agent skills
│   ├── .venv/       # Python virtual environment
│   └── requirements.txt
├── frontend/         # Vue 3 frontend
│   └── src/
├── desktop/         # Electron desktop application packaging
└── .env             # Root configuration file (read by the backend)
```

## Quick Start

### 1. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set your API credentials (or configure local Ollama endpoint):

```
OPENAI_API_KEY=sk-...
# Or for local Ollama / LM Studio:
# OPENAI_BASE_URL=http://localhost:11434/v1
# OPENAI_API_KEY=ollama
# OPENAI_MODEL=qwen2.5:7b
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv .venv
# On Linux/macOS:
source .venv/bin/activate
# On Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Running the Services

**Backend** (port 8011):

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8011
```

**Frontend** (proxied to `http://127.0.0.1:8011`):

```bash
cd frontend
npm run dev
```

## Workflow Patterns

| Type | Description |
|------|-------------|
| `single_agent_chat` | Single agent direct conversation with optional finalizer synthesizer |
| `router_specialists` | Router classifies user intent and selects the optimal specialist agent |
| `planner_executor` | Planner → Validator → Dispatcher → Worker Execution → Final Synthesizer |
| `supervisor_dynamic` | Supervisor dynamically evaluates progress and orchestrates cyclical delegation |
| `peer_handoff` | Decentralized agents dynamically hand off execution contexts to peer specialists |

## Desktop Packaging

Package the application as a standalone Electron desktop app (backend bundled using PyInstaller).

Prerequisites:

```bash
# Install PyInstaller in the backend venv
cd backend
source .venv/bin/activate
pip install -r requirements-desktop.txt
```

**macOS** (Local unsigned build):

```bash
cd desktop
npm install
npm run dist:mac
```

**macOS** (Signed release build):

```bash
cd desktop
npm run dist:mac:signed
```

**Windows**:

```bash
cd desktop
npm install
npm run dist:win
```

Build artifacts are output to `desktop/release/`.

## Notes
- Skills are stored in `backend/skills/`
- SQLite database is located at `backend/data/playground.db`
