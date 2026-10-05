"""Your first agent: a task-list assistant you talk to in the terminal.

How it works (the "agent loop"):
  1. You type a message.
  2. Claude reads it and decides whether to call one of the tools below.
  3. The SDK's tool runner runs the tool and sends the result back to Claude.
  4. Steps 2-3 repeat until Claude has nothing left to do, then it replies.

Run it:  python agent.py
"""

import json
import os
from pathlib import Path

import anthropic
from anthropic import beta_tool

from tasks import TaskStore

MODEL = "claude-opus-5-5"

SYSTEM_PROMPT = """You are a friendly assistant that manages the user's to-do list.
Use the tools to read and change the list; never guess what is on it.
Keep replies short. When you change the list, say what you changed."""

store = TaskStore(Path(os.environ.get("TASKS_FILE", Path(__file__).parent / "tasks.json")))


# --- Tools -----------------------------------------------------------------
# @beta_tool turns a typed Python function into a tool Claude can call. The
# docstring becomes the tool description and the Args section describes each
# parameter, so write them for Claude to read.


@beta_tool
def list_tasks() -> str:
    """List every task on the to-do list, with its id and whether it is done."""
    return json.dumps(store.list())


@beta_tool
def add_task(title: str) -> str:
    """Add a new task to the to-do list.

    Args:
        title: A short description of the task, e.g. "Buy milk".
    """
    return json.dumps(store.add(title))


@beta_tool
def complete_task(task_id: int) -> str:
    """Mark a task as done.

    Args:
        task_id: The id of the task, as returned by list_tasks.
    """
    task = store.complete(task_id)
    return json.dumps(task) if task else f"Error: no task with id {task_id}."


@beta_tool
def delete_task(task_id: int) -> str:
    """Delete a task from the to-do list permanently.

    Args:
        task_id: The id of the task, as returned by list_tasks.
    """
    task = store.delete(task_id)
    return json.dumps(task) if task else f"Error: no task with id {task_id}."


TOOLS = [list_tasks, add_task, complete_task, delete_task]


# --- Agent loop --------------------------------------------------------------


def run_turn(client: anthropic.Anthropic, messages: list) -> None:
    """Let Claude work on the latest user message until it is done."""
    runner = client.beta.messages.tool_runner(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        tools=TOOLS,
        messages=messages,
        output_config={"effort": "medium"},
        # If Claude's safety checks decline a request, retry it on a
        # recommended fallback model instead of failing.
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )

    last = None
    for message in runner:
        last = message
        # The runner keeps its own copy of the conversation, so we mirror it
        # here to remember everything for the next thing you type.
        messages.append({"role": "assistant", "content": message.content})
        tool_response = runner.generate_tool_call_response()
        if tool_response is not None:
            messages.append(tool_response)

        for block in message.content:
            if block.type == "tool_use":
                print(f"  [tool] {block.name}({json.dumps(block.input)})")
            elif block.type == "text" and block.text.strip():
                print(f"\nClaude: {block.text}\n")

    if last is not None and last.stop_reason == "refusal":
        print("\nClaude declined that request. Try rephrasing it.\n")


def main() -> None:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    messages: list = []

    print("Task agent ready. Ask me to add, list, complete, or delete tasks.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in {"quit", "exit"}:
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        try:
            run_turn(client, messages)
        except anthropic.AuthenticationError:
            print("\nYour API key was rejected. Check ANTHROPIC_API_KEY.\n")
            break
        except anthropic.RateLimitError:
            print("\nRate limited. Wait a moment and try again.\n")
            messages.pop()
        except anthropic.APIStatusError as e:
            print(f"\nAPI error {e.status_code}: {e.message}\n")
            messages.pop()
        except anthropic.APIConnectionError:
            print("\nCouldn't reach the API. Check your network connection.\n")
            messages.pop()


if __name__ == "__main__":
    main()
