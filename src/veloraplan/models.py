from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Goal(BaseModel):
    goal: str

class Scope(BaseModel):
    includes: List[str]
    excludes: List[str]

class ProjectCharter(BaseModel):
    title: str
    sponsor: str
    manager: str
    start_date: str
    end_date: str
    budget: float
    business_need: str
    goals: List[str]
    scope: Scope
    assumptions: List[str]
    constraints: List[str]
    stakeholders: List[str]

class Phase(BaseModel):
    name: str
    duration_days: int
    deliverables: List[str]

class Risk(BaseModel):
    id: str
    description: str
    likelihood: str
    impact: str
    mitigation: str

class PrioritizationItem(BaseModel):
    item: str
    impact: int = Field(ge=1, le=5)
    urgency: int = Field(ge=1, le=5)
    complexity: int = Field(ge=1, le=5)
    score: int

class ResourceAllocation(BaseModel):
    role: str
    allocation: List[int]  # FTE allocation per phase

class StakeholderComm(BaseModel):
    stakeholder: str
    needs: str
    frequency: str
    channel: str

class FinancialLine(BaseModel):
    category: str
    planned: float
    actual: Optional[float] = None
    variance: Optional[float] = None

class ProjectConfig(BaseModel):
    project_charter: ProjectCharter
    project_phases: List[Phase]
    risks: List[Risk]
    prioritization_analysis: List[PrioritizationItem]
    resource_allocation: List[ResourceAllocation]
    stakeholder_communications: List[StakeholderComm]
    financials: List[FinancialLine]

class ProjectStatus(BaseModel):
    current_phase: str
    phase_progress: float = Field(ge=0, le=100)
    overall_progress: float = Field(ge=0, le=100)
    budget_consumed: float
    risks_identified: int
    risks_mitigated: int
    last_updated: datetime = Field(default_factory=datetime.now)

class Deliverable(BaseModel):
    name: str
    phase: str
    status: str = "Not Started"  # Not Started, In Progress, Completed, Delayed
    due_date: Optional[str] = None
    owner: Optional[str] = None
    dependencies: List[str] = []
    notes: Optional[str] = None 