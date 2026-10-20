# AgentOS — AI Agent Engine

**A modular Python engine for task planning, tool execution, validation, and controlled AI agent workflows.**

AgentOS is an actively developed project focused on building the core engine behind a reliable and extensible AI agent platform. It provides tools for breaking goals into executable steps, validating tool arguments, managing execution, handling temporary failures, and supporting human approval for sensitive operations.

> **Project status:** Early development  
> **Current tests:** 40 passing automated tests

## Features

- **Task Planning:** Converts user goals into structured execution steps.
- **Tool Registry:** Registers tools and manages their metadata and argument requirements.
- **Argument Validation:** Uses Pydantic to validate tool inputs.
- **JSON Schema Generation:** Generates schemas describing the arguments accepted by registered tools.
- **Task Execution:** Executes planned steps and tracks task status.
- **Retry Handling:** Retries operations that encounter temporary failures.
- **Human Approval:** Supports approval workflows for sensitive operations.
- **Automated Testing:** Uses pytest to verify core functionality.

## Technology Stack

- Python 3.14
- Pydantic
- Pytest
- SQLAlchemy

## Project Structure

```text
agentos/
├── agent_engine/
│   ├── tools/
│   │   └── registry.py
│   ├── agent.py
│   ├── executor.py
│   └── planner.py
├── tests/
│   ├── test_agent_engine.py
│   ├── test_storage.py
│   ├── test_tool_planner.py
│   └── test_tool_registry.py
├── .gitignore
├── pyproject.toml
└── README.md
```

*The structure above illustrates the main project components; your local repository may contain additional files.*

## Getting Started

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd agentos
```

Replace the placeholder with your actual repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the project's dependencies according to the configuration in `pyproject.toml`. If the project defines its dependencies there, you can generally run:

```bash
python -m pip install -e ".[dev]"
```

### 4. Run the tests

```bash
python -m pytest -v
```

The current development baseline is **40 passing tests**. Your results may differ if the code changes.

## Development Roadmap

- Strengthen tool argument validation.
- Expand automated test coverage.
- Improve planning and execution capabilities.
- Develop backend API and authentication integration.
- Integrate database services and a dashboard.
- Prepare the platform for deployment.

## Project Goals

AgentOS aims to provide a maintainable foundation for AI agents that can understand goals, plan actions, execute registered tools, recover from temporary failures, and request human approval when appropriate.

The project is being developed incrementally, with reliability, modularity, and controlled execution as key priorities.

## Contributing

Suggestions, bug reports, and contributions are welcome. Please test changes before submitting them and avoid committing credentials, API keys, or other sensitive information.

## License

No license has been specified yet. Until a license is added, the repository should not be assumed to grant permission to reuse or redistribute its code.

---

**AgentOS — Building the foundation for reliable AI agents, one step at a time.**