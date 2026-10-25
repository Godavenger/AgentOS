
from agent_engine.state import AgentState, AgentStatus, PlanStep


def create_plan(state: AgentState) -> AgentState:
    """Create a basic structured plan from a user's goal."""

    goal = state.goal.strip()

    if not goal:
        raise ValueError("Task goal cannot be empty.")

    state.status = AgentStatus.PLANNING
    lower_goal = goal.lower()

    if any(word in lower_goal for word in ("calculate", "add", "multiply")):
        descriptions = [
            f"Understand the calculation requested: {goal}",
            "Perform the calculation using an appropriate tool.",
            "Check the result and prepare the final answer.",
        ]

    elif any(word in lower_goal for word in ("file", "document", "report")):
        descriptions = [
            f"Identify the required operation: {goal}",
            "Prepare the required changes.",
            "Validate the result and summarize the changes.",
        ]

    elif any(word in lower_goal for word in ("research", "find", "compare")):
        descriptions = [
            f"Identify the information needed: {goal}",
            "Gather and organize relevant information.",
            "Check the findings and prepare a summary.",
        ]

    else:
        descriptions = [
            f"Analyze the task: {goal}",
            "Determine and execute the required actions.",
            "Validate the result and prepare the final output.",
        ]

    state.steps = [
        PlanStep(
            step_id=index,
            description=description,
        )
        for index, description in enumerate(descriptions, start=1)
    ]

    state.current_step = 0
    state.result = None
    state.error = None
    state.status = AgentStatus.PENDING

    return state
