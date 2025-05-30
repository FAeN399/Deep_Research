# Deep Research Lab Overview

This project provides a lightweight space for running AI summarization over research notes.
Each collaborator maintains a profile with a `research/` folder and matching `ai_insights/` output.

## Usage

1. Drop markdown notes in `research/` or `profiles/<name>/research/`.
2. Run `python scripts/run_agent.py --profile <name>` to generate summaries.
3. Updated insights appear under the corresponding `ai_insights` folder.

## Contributing

- Keep changes in markdown files small and focused.
- After editing, run the agent so the summaries stay up to date.
- Submit your updates through version control.
