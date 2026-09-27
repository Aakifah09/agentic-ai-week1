def reflect(client, goal, answer):
    """
    Ask the LLM to check the proposed answer.

    The model should return:

        CONFIRM

    if the answer is correct, or:

        REVISE: <one sentence explaining what is wrong>

    if the answer is incorrect.
    """

    critique_prompt = (
        f"Goal: {goal}\n"
        f"Proposed Answer: {answer}\n\n"

        "You are checking the final answer of another agent.\n"
        "Decide whether the proposed answer is correct.\n\n"

        "STRICT OUTPUT RULES:\n"
        "If the proposed answer is CORRECT, output exactly:\n"
        "CONFIRM\n\n"

        "If the proposed answer is WRONG, output exactly:\n"
        "REVISE: <one short sentence explaining the error>\n\n"

        "IMPORTANT:\n"
        "If you determine that the proposed answer is correct, "
        "you MUST output CONFIRM.\n"
        "Never output REVISE when you say that the answer is correct.\n"
        "Do not explain your reasoning.\n"
        "Do not output anything else."
    )

    reply = client.get_completion(
        critique_prompt,
        temperature=0.0,
        max_tokens=50
    )

    if not reply:
        return "CONFIRM"

    # Get the first non-empty line
    lines = [
        line.strip()
        for line in reply.strip().splitlines()
        if line.strip()
    ]

    if not lines:
        return "CONFIRM"

    verdict = lines[0]
    upper_verdict = verdict.upper()

    # ---------------------------------------------------------
    # Correct response
    # ---------------------------------------------------------

    if upper_verdict.startswith("CONFIRM"):
        return "CONFIRM"

    # ---------------------------------------------------------
    # Handle contradictory Qwen response
    #
    # Example:
    # REVISE: ... the proposed answer is actually correct ...
    # ---------------------------------------------------------

    if upper_verdict.startswith("REVISE"):

        contradiction_phrases = [
            "ANSWER IS ACTUALLY CORRECT",
            "PROPOSED ANSWER IS ACTUALLY CORRECT",
            "ANSWER IS CORRECT",
            "PROPOSED ANSWER IS CORRECT",
            "THE ANSWER IS CORRECT",
            "THE PROPOSED ANSWER IS CORRECT"
        ]

        for phrase in contradiction_phrases:
            if phrase in upper_verdict:
                return "CONFIRM"

        return verdict

    # ---------------------------------------------------------
    # Unexpected response
    # ---------------------------------------------------------

    return "REVISE: The answer format was unclear. Recheck the calculation."
"""
05 · Reflection — make the agent check its own work.

The agent:
observe -> reason -> act -> evaluate -> REFLECT

If the reflection confirms the answer, the agent stops.
If reflection asks for a revision, the agent continues.
"""

import sys
import os
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.llm_client import LLMClient


def calculator(expression: str):
    return eval(expression, {"__builtins__": {}}, {})


SYSTEM = """You are a reasoning agent that solves a task step by step.

You have ONE tool:

calculator[expression] -> evaluates a math expression.

At EACH step reply with EXACTLY ONE line:

ACTION: calculator[<expression>]

OR

FINAL: <the final answer>

Take only ONE action at a time.
Use the observations you are given.
"""


MAX_STEPS = 8


def reflect(client, goal, answer):
    """
    Ask the LLM to check the proposed answer.

    It must return either:
    CONFIRM

    or:

    REVISE: <what is wrong>
    """

    critique_prompt = f"""
You are checking an answer produced by another reasoning agent.

Goal:
{goal}

Proposed Answer:
{answer}

Calculate the answer yourself and compare it with the proposed answer.

IMPORTANT:
If the proposed answer is correct, reply with EXACTLY:

CONFIRM

If the proposed answer is wrong, reply with EXACTLY:

REVISE: <one short sentence explaining the mistake>

Do not add anything else.
"""

    reply = client.get_completion(
        critique_prompt,
        temperature=0.0,
        max_tokens=50
    )

    reply = (reply or "").strip()

    print(f"        raw reflection: {reply}")

    if not reply:
        return "CONFIRM"

    first_line = reply.splitlines()[0].strip()

    # Normal correct response
    if first_line.upper() == "CONFIRM":
        return "CONFIRM"

    # If the model says REVISE but its explanation
    # clearly admits that the answer is correct,
    # treat it as CONFIRM.
    upper_reply = reply.upper()

    correct_phrases = [
        "ANSWER IS ACTUALLY CORRECT",
        "PROPOSED ANSWER IS ACTUALLY CORRECT",
        "ANSWER IS CORRECT",
        "PROPOSED ANSWER IS CORRECT",
        "THE ANSWER IS CORRECT",
        "THE PROPOSED ANSWER IS CORRECT",
        "ANSWER IS INDEED CORRECT",
        "PROPOSED ANSWER IS INDEED CORRECT"
    ]

    if first_line.upper().startswith("REVISE"):
        for phrase in correct_phrases:
            if phrase in upper_reply:
                return "CONFIRM"

        return first_line

    # Unexpected response
    return "REVISE: The reflection format was unclear. Recheck the calculation."


def run_agent(goal: str):

    print(f"\nGOAL: {goal}")
    print("-" * 60)

    client = LLMClient()

    history = ""

    for step in range(1, MAX_STEPS + 1):

        prompt = f"""
Task: {goal}

{history}

What is your next step?
"""

        response = client.get_completion(
            prompt,
            system_message=SYSTEM,
            temperature=0.0,
            max_tokens=200
        )

        line = (
            (response or "")
            .strip()
            .splitlines()[0]
            .strip()
        )

        print(f"[step {step}] {line}")

        # ------------------------------------------------
        # FINAL ANSWER
        # ------------------------------------------------

        if line.upper().startswith("FINAL:"):

            answer = line.split(":", 1)[1].strip()

            verdict = reflect(
                client,
                goal,
                answer
            )

            print(f"        reflection: {verdict}")

            if verdict.upper().startswith("CONFIRM"):

                return answer

            else:

                history += (
                    f"\nThe previous answer was '{answer}'. "
                    f"The reflection said: {verdict}. "
                    f"Recheck the calculation and try again."
                )

                continue

        # ------------------------------------------------
        # CALCULATOR ACTION
        # ------------------------------------------------

        match = re.search(
            r"calculator\[(.+?)\]",
            line
        )

        if match:

            expression = match.group(1)

            try:
                result = calculator(expression)

            except Exception as e:
                result = f"error: {e}"

            print(
                f"        observation: "
                f"calculator[{expression}] = {result}"
            )

            history += (
                f"\nYou ran calculator[{expression}] "
                f"and got {result}."
            )

        else:

            history += (
                "\n(No valid action found. "
                "Reply with ACTION: or FINAL:)"
            )

    return "Stopped: reached the step limit without a confirmed answer."


# ========================================================
# MAIN
# ========================================================

if __name__ == "__main__":

    goal = "What is (23 * 7) + 19?"

    print("Starting reflection agent...")

    final_answer = run_agent(goal)

    print("\nFINAL:", final_answer)