# Task agent

Your first AI agent: a command-line assistant that manages a to-do list.
You talk to it in plain English, and it uses **tools** (Python functions) to
read and change the list.

```
You: add buy milk and walk the dog, then show me my list
  [tool] add_task({"title": "Buy milk"})
  [tool] add_task({"title": "Walk the dog"})
  [tool] list_tasks({})

Claude: Added both. You have 2 open tasks: 1. Buy milk, 2. Walk the dog.
```

## What makes it an agent

A chatbot only replies with text. An agent can **act**: Claude decides which
tool to call, your code runs it, Claude reads the result and decides what to do
next, and this repeats until the job is done. That repeat cycle is the
*agent loop*. The Anthropic SDK's tool runner
(`client.beta.messages.tool_runner`) runs the loop for you.

## Files

| File | What it does |
|---|---|
| `agent.py` | The tools (`@beta_tool` functions) and the chat loop |
| `tasks.py` | Saves tasks to `tasks.json`; plain Python, no AI |
| `test_tasks.py` | Tests for the task store |

## Run it

You need Python 3.10+ and an Anthropic API key from
<https://platform.claude.com/settings/keys>.

```sh
cd agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python agent.py
```

Tasks are saved to `agent/tasks.json`. Set `TASKS_FILE` to use a different
file.

To run the tests (no API key needed):

```sh
pip install pytest
python -m pytest
```

## Ideas for what to try next

1. **Add a tool.** Write a `rename_task(task_id: int, title: str)` function
   with `@beta_tool`, add it to `TOOLS`, and ask Claude to rename something.
   The docstring is how Claude learns what the tool does.
2. **Add a field.** Give tasks a due date in `tasks.py` and update `add_task`
   so Claude can set it ("remind me to pay rent on the 1st").
3. **Change its personality** by editing `SYSTEM_PROMPT`.
4. **Ask for confirmation** before `delete_task` runs, using `input()` inside
   the tool.

Each request is billed to your API account. This agent uses
`claude-opus-5-5` at `medium` effort; you can change `MODEL` in `agent.py`.
