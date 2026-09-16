# Non LLM based parallel workflow

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class EmployeeState(TypedDict):
    employee_name: str
    monthly_salary: int
    working_days: int
    completed_projects: int

    yearly_salary: int
    bonus_amount: int
    project_status: str
    summary: str


# Nodes
def calculate_bonus(state: EmployeeState) -> dict:
    bonus = state["monthly_salary"] * 2
    return {"bonus_amount": bonus}


def calculate_yearly_salary(state: EmployeeState) -> dict:
    yearly_salary = state["monthly_salary"] * 12  # + state["bonus_amount"]
    return {"yearly_salary": yearly_salary}


def project_evaluation(state: EmployeeState) -> dict:
    completed_projects = state["completed_projects"]
    if completed_projects >= 7:
        status = "Excelent"
    elif completed_projects >= 5:
        status = "Good"
    elif completed_projects >= 3:
        status = "average"
    else:
        status = "poor"

    return {"project_status": status}


def summary(state: EmployeeState) -> dict:
    summary = f"Employee {state['employee_name']}, has completed {state['completed_projects']} projects this year, and has {state['project_status']} status, and have received {state['yearly_salary']} salary this year."
    return {"summary": summary}


graph = StateGraph(EmployeeState)

graph.add_node("calculate_bonus", calculate_bonus)
graph.add_node("calculate_yearly_salary", calculate_yearly_salary)
graph.add_node("project_evaluation", project_evaluation)
graph.add_node("summary", summary)


graph.add_edge(START, "calculate_bonus")
graph.add_edge(START, "calculate_yearly_salary")
graph.add_edge(START, "project_evaluation")


graph.add_edge("calculate_bonus", "summary")
graph.add_edge("calculate_yearly_salary", "summary")
graph.add_edge("project_evaluation", "summary")

graph.add_edge("summary", END)

workflow = graph.compile()

initial_state = {
    "employee_name": "John",
    "monthly_salary": 50000,
    "working_days": 275,
    "completed_projects": 5,
}

response = workflow.invoke(initial_state)

print(response)
