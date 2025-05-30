#!/usr/bin/env python3
"""CLI tool for embedding research notes and generating summaries."""

# This script reads markdown files, generates embeddings and a short summary
# using OpenAI APIs, and stores the results in matching `ai_insights` files.
# A unified diff is printed when a summary changes so collaborators can review
# updates before committing them.
import argparse
import os
import difflib
from pathlib import Path
import openai
from utils import load_yaml


def replace_insights(text, summary):
    """Return new file content with updated summary under '## Insights'."""
    lines = text.splitlines()
    try:
        i = lines.index("## Insights")
    except ValueError:
        lines += ["", "## Insights"]
        i = len(lines) - 1
    j = len(lines)
    for k in range(i + 1, len(lines)):
        if lines[k].startswith("## "):
            j = k
            break
    old = "\n".join(lines[i + 1:j]).strip()
    new_lines = lines[: i + 1] + [summary, ""] + lines[j:]
    return "\n".join(new_lines), old


def process(md_path, insight_dir, cfg, store):
    """Generate embedding and summary for a single markdown file."""
    text = Path(md_path).read_text(encoding="utf-8")
    store[str(md_path)] = openai.Embedding.create(
        model=cfg["embedding_model"], input=text
    )["data"][0]["embedding"]
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Summarize in one paragraph."},
            {"role": "user", "content": text},
        ],
    )["choices"][0]["message"]["content"].strip()
    template = insight_dir / "meta_analysis_template.md"
    target = insight_dir / f"{Path(md_path).stem}_analysis.md"
    if not target.exists():
        target.write_text(template.read_text())
    content = target.read_text(encoding="utf-8")
    new_content, old = replace_insights(content, summary)
    if old != summary:
        diff = difflib.unified_diff(
            old.splitlines(), summary.splitlines(),
            fromfile="previous", tofile="current", lineterm=""
        )
        print("\n".join(diff))
    target.write_text(new_content)


def gather(args):
    """Collect markdown paths and insight directory based on CLI args."""
    if args.file:
        p = Path(args.file)
        if "profiles" in p.parts:
            idx = p.parts.index("profiles")
            insight = Path("profiles") / p.parts[idx + 1] / "ai_insights"
        else:
            insight = Path("ai_insights")
        return [p], insight
    if args.profile:
        base = Path("profiles") / args.profile
        return list((base / "research").glob("*.md")), base / "ai_insights"
    return list(Path("research").glob("*.md")), Path("ai_insights")


def main():
    """Parse arguments and process markdown files."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile")
    parser.add_argument("--file")
    args = parser.parse_args()
    cfg = load_yaml("config.yml")
    # Ensure the environment has the OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found")
        return
    files, insight_dir = gather(args)
    # Store embeddings in memory; persisting them is outside the scope here
    embeddings = {}
    for path in files:
        process(path, insight_dir, cfg, embeddings)


if __name__ == "__main__":
    main()
