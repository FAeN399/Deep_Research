# Deep Research Lab

Private AI-assisted research environment for Repo Man and The Prince. Use the agent to summarize research notes and track insights.

## Quick Start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your OpenAI key
make run PROFILE=repo_man
```

## How to Run

```bash
python scripts/run_agent.py              # process global research
python scripts/run_agent.py --profile repo_man  # specific profile
make run PROFILE=repo_man               # via Makefile
```

### Creating a New Profile
1. `cp -R profiles/repo_man profiles/<your_name>`
2. Add docs to `profiles/<your_name>/research/`
3. `python scripts/run_agent.py --profile <your_name>`
