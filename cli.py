
import argparse

from agent_engine.agent import run_agent
from agent_engine.storage.repository import get_task, list_tasks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AgentOS - AI Agent Engine"
    )

    parser.add_argument(
        "goal",
        nargs="*",
        help="Task to execute, or use history/show commands",
    )

    args = parser.parse_args()
    parts = args.goal

    if not parts:
        parser.print_help()
        return

    command = parts[0].lower()

    if command == "history":
        tasks = list_tasks()

        if not tasks:
            print("No saved tasks found.")
            return

        print("\nSaved task history:")
        for task in tasks:
            print(
                f"\nTask ID: {task['task_id']}"
                f"\nGoal: {task['goal']}"
                f"\nStatus: {task['status']}"
                f"\nResult: {task['result']}"
            )
        return

    if command == "show":
        if len(parts) != 2:
            parser.error("Usage: python -m agent_engine.cli show TASK_ID")

        task = get_task(parts[1])

        if task is None:
            print(f"Task not found: {parts[1]}")
            return

        print(f"\nTask ID: {task['task_id']}")
        print(f"Goal: {task['goal']}")
        print(f"Status: {task['status']}")
        print(f"Result: {task['result']}")

        if task["error"]:
            print(f"Error: {task['error']}")

        print("\nExecution history:")
        for event in task["execution_log"]:
            print(f"- {event}")
        return

    goal = " ".join(parts)
    state = run_agent(goal)

    print(f"\nTask: {state.goal}")
    print(f"Task ID: {state.task_id}")
    print(f"Status: {state.status.value}")

    if state.result is not None:
        print(f"Result: {state.result}")

    if state.error:
        print(f"Error: {state.error}")

    if state.execution_log:
        print("\nExecution history:")
        for event in state.execution_log:
            print(f"- {event}")


if __name__ == "__main__":
    main()
