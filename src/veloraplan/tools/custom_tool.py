# Custom tools for CrewAI project pipeline
from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import json

# --- Tool 1: Scoring Calculator Tool ---
class ScoringInput(BaseModel):
    score: int = Field(..., description="Total score from intake scoring")
    criticality_multiplier: float = Field(..., description="Business criticality multiplier")

class ScoringCalculatorTool(BaseTool):
    name: str = "Scoring Calculator Tool"
    description: str = (
        "Calculates weighted score and assigns a priority tier (P1–P4) based on business rules."
    )
    args_schema: Type[BaseModel] = ScoringInput

    def _run(self, score: int, criticality_multiplier: float) -> str:
        weighted_score = score * criticality_multiplier
        if weighted_score >= 18:
            priority = "P1"
        elif weighted_score >= 12:
            priority = "P2"
        elif weighted_score >= 6:
            priority = "P3"
        else:
            priority = "P4"
        return json.dumps({
            "weighted_score": weighted_score,
            "priority": priority
        })

# --- Tool 2: Mermaid Gantt Generator Tool ---
class GanttInput(BaseModel):
    tasks: List[str] = Field(..., description="A list of tasks with durations in the format 'Task Name:StartDay:Duration'")

class MermaidGanttGeneratorTool(BaseTool):
    name: str = "Mermaid Gantt Generator Tool"
    description: str = "Generates Mermaid-compatible Gantt chart syntax from a list of tasks."
    args_schema: Type[BaseModel] = GanttInput

    def _run(self, tasks: List[str]) -> str:
        lines = ["gantt", "    title Project Timeline", "    dateFormat  YYYY-MM-DD"]
        day_offset = 0
        for t in tasks:
            name, start, duration = t.split(":")
            lines.append(f"    {name} :done, des{day_offset}, {start}, {duration}d")
            day_offset += 1
        return "\n".join(lines)

# --- Tool 3: Project Charter Formatter Tool ---
class CharterInput(BaseModel):
    project_title: str
    objectives: str
    scope: str
    timeline_summary: str
    risks: str

class CharterFormatterTool(BaseTool):
    name: str = "Charter Formatter Tool"
    description: str = "Generates a clean project charter in markdown format from structured inputs."
    args_schema: Type[BaseModel] = CharterInput

    def _run(self, project_title: str, objectives: str, scope: str, timeline_summary: str, risks: str) -> str:
        return f"""
# Project Charter: {project_title}

## Objectives
{objectives}

## Scope
{scope}

## Timeline Summary
{timeline_summary}

## Risks & Assumptions
{risks}
"""

# --- Tool 4: Resource Allocation Table Tool ---
class ResourceAllocationInput(BaseModel):
    assignments: List[str] = Field(..., description="List of assignments in format 'Role: Week X: FTEs'")

class ResourceAllocationFormatterTool(BaseTool):
    name: str = "Resource Allocation Formatter Tool"
    description: str = "Formats resource assignment strings into a readable table or summary."
    args_schema: Type[BaseModel] = ResourceAllocationInput

    def _run(self, assignments: List[str]) -> str:
        output = ["## Resource Allocation Plan"]
        for row in assignments:
            output.append(f"- {row}")
        return "\n".join(output)
