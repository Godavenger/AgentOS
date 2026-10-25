
from agent_engine.state import AgentState, AgentStatus
from agent_engine.tools.registry import ToolRegistry


TERMINAL_STATUSES = {
    AgentStatus.COMPLETED,
    AgentStatus.FAILED,
    AgentStatus.WAITING_FOR_APPROVAL,
}


def format_result(result: object) -> str:
    """Convert a tool result to its standard string representation."""
    return str(result)


def execute_next_step(
    state: AgentState,
    registry: ToolRegistry,
    max_retries: int = 2,
) -> AgentState:
    """Execute the next step with retries and approval checks."""

    if max_retries < 0:
        raise ValueError("max_retries cannot be negative.")

    if state.status in TERMINAL_STATUSES:
        return state

    if not state.steps:
        state.status = AgentStatus.FAILED
        state.error = "No plan available."
        state.execution_log.append(state.error)
        return state

    if state.current_step >= len(state.steps):
        state.status = AgentStatus.COMPLETED
        return state

    step = state.steps[state.current_step]

    state.execution_log.append(
        f"Starting step {step.step_id}: {step.description}"
    )

    if step.requires_approval and not step.approved:
        state.status = AgentStatus.WAITING_FOR_APPROVAL
        state.error = None
        state.execution_log.append(
            f"Step {step.step_id} is waiting for human approval."
        )
        return state

    if not step.tool_name:
        state.error = f"Step {step.step_id} has no tool assigned."
        state.status = AgentStatus.FAILED
        state.execution_log.append(state.error)
        return state

    state.status = AgentStatus.RUNNING
    last_error = None
    attempts_made = 0

    for attempt in range(max_retries + 1):
        attempts_made = attempt + 1

        try:
            result = registry.execute(
                step.tool_name,
                **step.tool_args,
            )

            state.result = format_result(result)
            step.completed = True
            state.current_step += 1
            state.error = None

            state.execution_log.append(
                f"Step {step.step_id} succeeded using "
                f"tool '{step.tool_name}' on attempt {attempt + 1}."
            )

            if state.current_step >= len(state.steps):
                state.status = AgentStatus.COMPLETED
                state.execution_log.append(
                    "Task completed successfully."
                )
            else:
                state.status = AgentStatus.PENDING

            return state

        except ValueError as error:
            # Invalid arguments and other ValueErrors are not retried.
            last_error = error
            state.execution_log.append(
                f"Step {step.step_id} failed permanently: "
                f"{type(error).__name__}: {error}"
            )
            break

        except Exception as error:
            # Unexpected errors may be temporary.
            last_error = error
            state.execution_log.append(
                f"Step {step.step_id}, attempt {attempt + 1} failed: "
                f"{type(error).__name__}: {error}"
            )

    state.error = (
        f"Tool '{step.tool_name}' failed after "
        f"{attempts_made} attempt(s): "
        f"{type(last_error).__name__}: {last_error}"
    )
    state.status = AgentStatus.FAILED
    state.execution_log.append(state.error)

    return state


def execute_plan(
    state: AgentState,
    registry: ToolRegistry,
    max_steps: int = 10,
    max_retries: int = 2,
) -> AgentState:
    """Execute a plan with step and retry limits."""

    if max_steps < 1:
        raise ValueError("max_steps must be at least 1.")

    steps_executed = 0

    while (
        state.current_step < len(state.steps)
        and steps_executed < max_steps
        and state.status not in TERMINAL_STATUSES
    ):
        previous_step = state.current_step

        execute_next_step(
            state,
            registry,
            max_retries=max_retries,
        )

        steps_executed += 1

        if state.current_step == previous_step:
            break

    if (
        state.status not in TERMINAL_STATUSES
        and state.current_step < len(state.steps)
    ):
        state.status = AgentStatus.FAILED
        state.error = f"Execution limit reached: {max_steps} steps."
        state.execution_log.append(state.error)

    return state


def approve_current_step(state: AgentState) -> AgentState:
    """Approve the current step so execution can continue."""

    if state.status != AgentStatus.WAITING_FOR_APPROVAL:
        raise ValueError("Agent is not waiting for approval.")

    if state.current_step >= len(state.steps):
        raise ValueError("No current step to approve.")

    step = state.steps[state.current_step]

    if not step.requires_approval:
        raise ValueError("Current step does not require approval.")

    step.approved = True
    state.status = AgentStatus.PENDING
    state.error = None

    state.execution_log.append(
        f"Step {step.step_id} approved by the user."
    )

    return state
