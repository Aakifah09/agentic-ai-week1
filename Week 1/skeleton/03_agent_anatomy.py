"""
03 · Agent anatomy — design a task-execution agent blueprint.

   >>> THIS IS  WEEK 1 DELIVERABLE. <<<

Every agent, from a toy to a production system, is made of four parts:
    GOAL      — what it's trying to achieve (and how we know it's done)
    TOOLS     — how it acts on the world (APIs, code, search, databases)
    MEMORY    — what it remembers between steps
    ACTIONS   — the sequence of steps it takes

A worked EXAMPLE is filled in for you below. Study it, then design YOUR OWN
agent for a real, repetitive, multi-step task you'd like to automate.

----------------------------------------------------------------------
 TASK
  TODO: Fill in `my_agent` with your own blueprint. Keep the task realistic
        and bounded. Be specific about `done_when` — a vague goal can't be
        evaluated. Then run the file to print your blueprint.
----------------------------------------------------------------------
No LLM/API key needed for this exercise — it's pure design.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class AgentBlueprint:
    name: str
    goal: str
    done_when: str
    tools: List[str] = field(default_factory=list)
    memory: List[str] = field(default_factory=list)
    actions: List[str] = field(default_factory=list)

    def show(self):
        print("=" * 60)
        print(f" AGENT BLUEPRINT: {self.name}")
        print("=" * 60)
        print(f"GOAL       : {self.goal}")
        print(f"DONE WHEN  : {self.done_when}")
        print("TOOLS      :")
        for t in self.tools:
            print(f"   - {t}")
        print("MEMORY     :")
        for m in self.memory:
            print(f"   - {m}")
        print("ACTIONS    :")
        for i, a in enumerate(self.actions, 1):
            print(f"   {i}. {a}")
        print()


# ----------------------------------------------------------------------
# WORKED EXAMPLE (already complete) — a restaurant-booking agent
# ----------------------------------------------------------------------
example = AgentBlueprint(
    name="Restaurant Booking Agent",
    goal="Book a dinner table for 4 people this Friday at 8 PM near the user.",
    done_when="A confirmed booking (with a reference number) exists, or the user is told none is available.",
    tools=[
        "restaurant_search(area, cuisine) -> list of places",
        "check_availability(place, date, time, party_size) -> bool",
        "make_booking(place, date, time, party_size) -> confirmation",
    ],
    memory=[
        "User preferences (cuisine, budget, location)",
        "Places already tried (so it doesn't repeat)",
        "The current best candidate",
    ],
    actions=[
        "Search restaurants matching the user's preferences",
        "For each candidate, check availability for Friday 8 PM, party of 4",
        "If available, make the booking and return the confirmation",
        "If none available, report back and suggest alternative times",
    ],
)


# ----------------------------------------------------------------------
# YOUR BLUEPRINT — Week 1 Deliverable
# ----------------------------------------------------------------------
my_agent = AgentBlueprint(
    name="Coursework Evaluation & Feedback Agent",
    goal="Automate the grading and critique of student Python lab submissions against defined rubrics and unit test suites.",
    done_when="All lab submissions in the grading queue have been executed through tests, code style evaluated, and structured feedback reports stored with an assigned score.",
    tools=[
        "fetch_submissions(assignment_id) -> list of student repos and file paths",
        "run_sandboxed_tests(submission_file, test_spec) -> execution status, pass/fail metrics, traceback logs",
        "ast_security_scanner(submission_file) -> list of unsafe builtins or banned modules",
        "evaluate_code_quality(code_snippet, rubric) -> score breakdown and syntax feedback",
        "save_grade_report(student_id, score, feedback_summary) -> confirmation ID",
    ],
    memory=[
        "Current assignment rubric, expected test outputs, and grading scale",
        "Queue of student submissions (pending, in-progress, completed)",
        "Execution logs, lint warnings, and runtime test results for the active student",
        "Aggregated common syntax errors and misconceptions across the cohort",
    ],
    actions=[
        "Poll the submission queue and retrieve the next pending student code file",
        "Scan the submission AST for security violations and forbidden imports",
        "Run the automated test suite in a sandboxed runtime to verify functional correctness",
        "Evaluate code structure, variable naming, and algorithmic efficiency against rubric criteria",
        "Synthesize comprehensive feedback combining test outputs, style tips, and scores",
        "Save the finalized grade report and update the submission status to graded",
    ],
)


if __name__ == "__main__":
    example.show()
    my_agent.show()
