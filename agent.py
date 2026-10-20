
from uuid import uuid4

from agent_engine.state import AgentState, AgentStatus
from agent_engine.tool_planner import create_tool_plan
from agent_engine.executor import execute_plan
from agent_engine.tools.registry import ToolRegistry
from agent_engine.tools.calculator import (
    add,
    multiply,
    subtract,
    divide,
    power,
)
from agent_engine.storage.repository import save_task


def build_registry() -> ToolRegistry:
    """Build the registry of tools available to the agent."""

    registry = ToolRegistry()

    registry.register("add", add, "Add two numbers.")
    registry.register("multiply", multiply, "Multiply two numbers.")
    registry.register(
        "subtract", subtract, "Subtract the second number from the first."
    )
    registry.register(
        "divide", divide, "Divide the first number by the second."
    )
    registry.register(
        "power", power, "Raise the first number to the power of the second."
    )

    return registry


def run_agent(goal: str) -> AgentState:
    """Plan, execute, and persist a task."""

    state = AgentState(task_id=str(uuid4()), goal=goal)

    try:
        registry = build_registry()
        create_tool_plan(state, registry)
        execute_plan(state, registry)
    except ValueError as error:
        state.status = AgentStatus.FAILED
        state.error = str(error)
        state.execution_log.append(f"Task failed: {error}")

    save_task(state)
    return state
