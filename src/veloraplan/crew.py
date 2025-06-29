# Custom tools for CrewAI project pipeline
from crewai.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import json
import yaml
from pathlib import Path
from crewai import Crew, Agent, Task, Process
from langchain_openai import ChatOpenAI
import os

# Import the new project configuration system
from veloraplan.project_loader import ProjectLoader, create_project_loader
from veloraplan.models import ProjectConfig

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("💡 Install python-dotenv for .env file support: pip install python-dotenv")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

# --- Cost Estimation Helper ---
class CostEstimator:
    """Helper class to estimate OpenAI API costs"""
    
    # gpt-4.1-nano pricing (as of 2024)
    INPUT_COST_PER_1K_TOKENS = 0.0005  # $0.0005 per 1K input tokens
    OUTPUT_COST_PER_1K_TOKENS = 0.0015  # $0.0015 per 1K output tokens
    
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.estimated_cost = 0.0
    
    def add_usage(self, input_tokens: int, output_tokens: int):
        """Add token usage to the estimator"""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self._calculate_cost()
    
    def _calculate_cost(self):
        """Calculate estimated cost based on current usage"""
        input_cost = (self.total_input_tokens / 1000) * self.INPUT_COST_PER_1K_TOKENS
        output_cost = (self.total_output_tokens / 1000) * self.OUTPUT_COST_PER_1K_TOKENS
        self.estimated_cost = input_cost + output_cost
    
    def get_estimate(self) -> dict:
        """Get current cost estimate"""
        return {
            "input_tokens": self.total_input_tokens,
            "output_tokens": self.total_output_tokens,
            "estimated_cost_usd": round(self.estimated_cost, 4),
            "estimated_cost_cents": round(self.estimated_cost * 100, 2)
        }
    
    def print_estimate(self):
        """Print current cost estimate"""
        estimate = self.get_estimate()
        print(f"\n💰 COST ESTIMATE:")
        print(f"   Input tokens: {estimate['input_tokens']:,}")
        print(f"   Output tokens: {estimate['output_tokens']:,}")
        print(f"   Estimated cost: ${estimate['estimated_cost_usd']} ({estimate['estimated_cost_cents']} cents)")

# Global cost estimator instance
cost_estimator = CostEstimator()

# --- Tool 1: Project Configuration Tool ---
class ProjectConfigInput(BaseModel):
    config_path: str = Field(default=None, description="Path to project configuration file")

class ProjectConfigTool(BaseTool):
    name: str = "Project Configuration Tool"
    description: str = "Loads and provides access to comprehensive project configuration including charter, phases, risks, and resources."
    args_schema: Type[BaseModel] = ProjectConfigInput

    def _run(self, config_path: str = None) -> str:
        try:
            loader = create_project_loader(config_path)
            config = loader.config
            
            # Return comprehensive project information
            project_info = {
                "project_charter": {
                    "title": config.project_charter.title,
                    "sponsor": config.project_charter.sponsor,
                    "manager": config.project_charter.manager,
                    "budget": config.project_charter.budget,
                    "business_need": config.project_charter.business_need,
                    "goals": config.project_charter.goals,
                    "scope": {
                        "includes": config.project_charter.scope.includes,
                        "excludes": config.project_charter.scope.excludes
                    }
                },
                "phases": [{"name": p.name, "duration_days": p.duration_days, "deliverables": p.deliverables} for p in config.project_phases],
                "risks": [{"id": r.id, "description": r.description, "likelihood": r.likelihood, "impact": r.impact, "mitigation": r.mitigation} for r in config.risks],
                "prioritization": [{"item": p.item, "score": p.score} for p in config.prioritization_analysis],
                "resources": [{"role": r.role, "allocation": r.allocation} for r in config.resource_allocation],
                "financials": [{"category": f.category, "planned": f.planned} for f in config.financials]
            }
            
            return json.dumps(project_info, indent=2)
        except Exception as e:
            return f"Error loading project configuration: {str(e)}"

# --- Tool 2: Enhanced Scoring Calculator Tool ---
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

# --- Tool 3: Enhanced Mermaid Gantt Generator Tool ---
class GanttInput(BaseModel):
    phases: List[dict] = Field(..., description="List of project phases with duration and deliverables")

class MermaidGanttGeneratorTool(BaseTool):
    name: str = "Mermaid Gantt Generator Tool"
    description: str = "Generates Mermaid-compatible Gantt chart syntax from project phases and deliverables."
    args_schema: Type[BaseModel] = GanttInput

    def _run(self, phases: List[dict]) -> str:
        lines = ["gantt", "    title Project Timeline", "    dateFormat  YYYY-MM-DD"]
        
        current_date = "2025-07-01"  # Start date from config
        day_offset = 0
        
        for phase in phases:
            phase_name = phase.get("name", "Unknown Phase")
            duration_days = phase.get("duration_days", 7)
            deliverables = phase.get("deliverables", [])
            
            # Add phase section
            clean_phase_name = phase_name.replace(" ", "_").replace("-", "_")
            lines.append(f"    section {phase_name}")
            
            # Add deliverables within the phase
            for deliverable in deliverables:
                clean_deliverable = deliverable.replace(" ", "_").replace("-", "_")
                lines.append(f"    {clean_deliverable} :done, des{day_offset}, {current_date}, {duration_days}d")
                day_offset += 1
        
        return "\n".join(lines)

# --- Tool 4: Enhanced Project Charter Formatter Tool ---
class CharterInput(BaseModel):
    project_config: dict = Field(..., description="Complete project configuration")

class CharterFormatterTool(BaseTool):
    name: str = "Charter Formatter Tool"
    description: str = "Generates a comprehensive project charter using the project configuration."
    args_schema: Type[BaseModel] = CharterInput

    def _run(self, project_config: dict) -> str:
        charter = project_config.get("project_charter", {})
        
        charter_text = f"""
# Project Charter: {charter.get('title', 'Project')}

## Executive Summary
{charter.get('business_need', 'Business need to be defined.')}

## Project Objectives
{chr(10).join([f"- {goal}" for goal in charter.get('goals', [])])}

## Project Scope
### Includes:
{chr(10).join([f"- {item}" for item in charter.get('scope', {}).get('includes', [])])}

### Excludes:
{chr(10).join([f"- {item}" for item in charter.get('scope', {}).get('excludes', [])])}

## Timeline
- **Start Date**: {charter.get('start_date', 'TBD')}
- **End Date**: {charter.get('end_date', 'TBD')}
- **Duration**: {charter.get('duration', 'TBD')}

## Budget
- **Total Budget**: ${charter.get('budget', 0):,.0f}

## Project Team
- **Sponsor**: {charter.get('sponsor', 'TBD')}
- **Manager**: {charter.get('manager', 'TBD')}

## Assumptions
{chr(10).join([f"- {assumption}" for assumption in charter.get('assumptions', [])])}

## Constraints
{chr(10).join([f"- {constraint}" for constraint in charter.get('constraints', [])])}

## Stakeholders
{chr(10).join([f"- {stakeholder}" for stakeholder in charter.get('stakeholders', [])])}
"""
        return charter_text

# --- Tool 5: Enhanced Resource Allocation Formatter Tool ---
class ResourceAllocationInput(BaseModel):
    resource_config: List[dict] = Field(..., description="Resource allocation configuration")

class ResourceAllocationFormatterTool(BaseTool):
    name: str = "Resource Allocation Formatter Tool"
    description: str = "Formats resource allocation configuration into a readable table."
    args_schema: Type[BaseModel] = ResourceAllocationInput

    def _run(self, resource_config: List[dict]) -> str:
        if not resource_config:
            return "No resource allocation data available."
        
        # Create phase headers
        phases = [f"Week {i+1}" for i in range(max(len(r.get('allocation', [])) for r in resource_config))]
        
        resource_table = "## Resource Allocation Plan\n\n"
        resource_table += "| Role | " + " | ".join(phases) + " |\n"
        resource_table += "|------|" + "|".join(["-----" for _ in phases]) + "|\n"
        
        for resource in resource_config:
            role = resource.get('role', 'Unknown')
            allocation = resource.get('allocation', [])
            row = f"| {role} |"
            for i, phase in enumerate(phases):
                fte = allocation[i] if i < len(allocation) else 0
                row += f" {fte} FTE |"
            resource_table += row + "\n"
        
        return resource_table

# --- Tool 6: Enhanced Risk Assessment Tool ---
class RiskAssessmentInput(BaseModel):
    risk_config: List[dict] = Field(..., description="Risk configuration from project config")

class RiskAssessmentTool(BaseTool):
    name: str = "Risk Assessment Tool"
    description: str = "Formats risk assessment configuration into a comprehensive risk register."
    args_schema: Type[BaseModel] = RiskAssessmentInput

    def _run(self, risk_config: List[dict]) -> str:
        if not risk_config:
            return "No risk assessment data available."
        
        risk_table = "## Risk Assessment and Mitigation Plan\n\n"
        risk_table += "| Risk ID | Description | Likelihood | Impact | Mitigation Strategy |\n"
        risk_table += "|---------|-------------|------------|--------|-------------------|\n"
        
        for risk in risk_config:
            risk_id = risk.get('id', 'Unknown')
            description = risk.get('description', 'No description')
            likelihood = risk.get('likelihood', 'Unknown')
            impact = risk.get('impact', 'Unknown')
            mitigation = risk.get('mitigation', 'No mitigation strategy')
            
            risk_table += f"| {risk_id} | {description} | {likelihood} | {impact} | {mitigation} |\n"
        
        return risk_table

# --- Tool 7: Enhanced Prioritization Analysis Tool ---
class PrioritizationInput(BaseModel):
    prioritization_config: List[dict] = Field(..., description="Prioritization configuration from project config")

class PrioritizationAnalysisTool(BaseTool):
    name: str = "Prioritization Analysis Tool"
    description: str = "Formats prioritization configuration into a comprehensive analysis."
    args_schema: Type[BaseModel] = PrioritizationInput

    def _run(self, prioritization_config: List[dict]) -> str:
        if not prioritization_config:
            return "No prioritization data available."
        
        # Sort by score descending
        sorted_items = sorted(prioritization_config, key=lambda x: x.get('score', 0), reverse=True)
        
        prioritization_table = "## Prioritization Analysis\n\n"
        prioritization_table += "| Item | Impact | Urgency | Complexity | Score |\n"
        prioritization_table += "|------|--------|---------|------------|-------|\n"
        
        for item in sorted_items:
            item_name = item.get('item', 'Unknown')
            impact = item.get('impact', 0)
            urgency = item.get('urgency', 0)
            complexity = item.get('complexity', 0)
            score = item.get('score', 0)
            
            prioritization_table += f"| {item_name} | {impact} | {urgency} | {complexity} | {score} |\n"
        
        return prioritization_table

# --- Tool 8: Enhanced Financial Tracking Tool ---
class FinancialInput(BaseModel):
    financial_config: List[dict] = Field(..., description="Financial configuration from project config")

class FinancialTrackingTool(BaseTool):
    name: str = "Financial Tracking Tool"
    description: str = "Formats financial configuration into a comprehensive budget tracking table."
    args_schema: Type[BaseModel] = FinancialInput

    def _run(self, financial_config: List[dict]) -> str:
        if not financial_config:
            return "No financial data available."
        
        financial_table = "## Financial Summary\n\n"
        financial_table += "| Category | Planned | Actual | Variance |\n"
        financial_table += "|----------|---------|--------|----------|\n"
        
        total_planned = 0
        total_actual = 0
        
        for financial in financial_config:
            category = financial.get('category', 'Unknown')
            planned = financial.get('planned', 0)
            actual = financial.get('actual', 0)
            variance = financial.get('variance', actual - planned)
            
            total_planned += planned
            total_actual += actual
            
            financial_table += f"| {category} | ${planned:,.0f} | ${actual:,.0f} | ${variance:,.0f} |\n"
        
        financial_table += f"| **Total** | **${total_planned:,.0f}** | **${total_actual:,.0f}** | **${total_actual - total_planned:,.0f}** |\n"
        
        return financial_table

# --- Tool 9: Enhanced Work Effort Estimator Tool ---
class WorkEffortInput(BaseModel):
    task_description: str = Field(..., description="A detailed description of the task")
    phase_context: str = Field(..., description="The phase context for the task")

class WorkEffortEstimatorTool(BaseTool):
    name: str = "Work Effort Estimator Tool"
    description: str = "Estimates the work effort (in hours) required for a described task within a specific phase."
    args_schema: Type[BaseModel] = WorkEffortInput

    def _run(self, task_description: str, phase_context: str) -> str:
        # Enhanced effort estimation based on task type, complexity, and phase
        base_hours = 8  # Base 1 day
        
        # Adjust based on phase
        phase_multipliers = {
            "Initiation": 0.5,
            "Planning": 1.0,
            "Discovery & Requirements": 1.5,
            "Design": 2.0,
            "Build & Configuration": 3.0,
            "Testing": 1.5,
            "Training & Adoption": 1.0,
            "Deployment": 1.0
        }
        
        phase_multiplier = phase_multipliers.get(phase_context, 1.0)
        
        # Adjust based on task complexity keywords
        complexity_keywords = {
            "high": 2.0, "complex": 2.0, "difficult": 1.8, "challenging": 1.5,
            "medium": 1.0, "standard": 1.0, "normal": 1.0,
            "low": 0.5, "simple": 0.5, "basic": 0.5, "easy": 0.5
        }
        
        complexity_multiplier = 1.0
        task_lower = task_description.lower()
        for keyword, multiplier in complexity_keywords.items():
            if keyword in task_lower:
                complexity_multiplier = multiplier
                break
        
        estimated_hours = base_hours * phase_multiplier * complexity_multiplier
        
        return json.dumps({
            "task": task_description,
            "phase": phase_context,
            "estimated_hours": round(estimated_hours, 1),
            "estimated_days": round(estimated_hours / 8, 1),
            "complexity_level": "High" if complexity_multiplier > 1.5 else "Medium" if complexity_multiplier > 0.8 else "Low"
        })

class Veloraplan:
    def __init__(self, config_path: str = None):
        self.config_path = config_path
        self.project_loader = None
        self.config = None
        
        # Initialize project configuration
        try:
            self.project_loader = create_project_loader(config_path)
            self.config = self.project_loader.config
            print(f"✅ Loaded project configuration: {self.config.project_charter.title}")
        except Exception as e:
            print(f"⚠️  Could not load project configuration: {e}")
            print("Using fallback configuration...")

    def _load_yaml(self, filename: str) -> dict:
        """Load YAML configuration file"""
        config_path = Path(__file__).parent / "config" / filename
        with open(config_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)

    def _create_agents(self, inputs: dict) -> dict:
        """Create agents using project configuration"""
        agents_config = self._load_yaml("agents.yaml")
        agents = {}
        
        # Get project context for agent customization
        project_title = inputs.get("project_title", "Project")
        project_type = inputs.get("type", "Transformation")
        
        for agent_name, agent_config in agents_config.items():
            # Customize agent with project-specific information
            role = agent_config["role"].format(project_type=project_type)
            goal = agent_config["goal"].format(project_type=project_type)
            backstory = agent_config["backstory"].format(project_type=project_type)
            
            # Add project-specific tools
            tools = []
            if agent_name == "project_planner_agent":
                tools = [
                    ProjectConfigTool(),
                    ScoringCalculatorTool(),
                    WorkEffortEstimatorTool()
                ]
            elif agent_name == "estimation_agent":
                tools = [
                    ProjectConfigTool(),
                    ScoringCalculatorTool(),
                    WorkEffortEstimatorTool()
                ]
            elif agent_name == "deliverable_agent":
                tools = [
                    ProjectConfigTool(),
                    CharterFormatterTool(),
                    MermaidGanttGeneratorTool(),
                    ResourceAllocationFormatterTool(),
                    RiskAssessmentTool(),
                    PrioritizationAnalysisTool(),
                    FinancialTrackingTool()
                ]
            
            agents[agent_name] = Agent(
                role=role,
                goal=goal,
                backstory=backstory,
                allow_delegation=agent_config.get("allow_delegation", False),
                verbose=agent_config.get("verbose", False),
                tools=tools
            )
        
        return agents

    def _create_tasks(self, agents: dict, inputs: dict) -> List[Task]:
        """Create tasks using project configuration"""
        tasks_config = self._load_yaml("tasks.yaml")
        tasks = []
        
        # Get project context
        project_title = inputs.get("project_title", "Project")
        
        for task_name, task_config in tasks_config.items():
            # Customize task with project-specific information
            description = task_config["description"].format(project_type=inputs.get("type", "Transformation"))
            expected_output = task_config["expected_output"]
            agent = agents[task_config["agent"]]
            
            # Add minimal project context to task
            if self.config:
                description += f"\n\nProject: {self.config.project_charter.title} | Budget: ${self.config.project_charter.budget:,.0f}"
            
            tasks.append(Task(
                description=description,
                expected_output=expected_output,
                agent=agent
            ))
        
        return tasks

    def crew(self) -> Crew:
        """Create and return the crew with project configuration"""
        # Get inputs from project configuration
        if self.project_loader:
            inputs = self.project_loader.get_crew_inputs()
        else:
            # Fallback to basic inputs
            inputs = {
                "project_id": "PRJ-001",
                "current_year": "2025",
                "project_title": "Project",
                "objectives": "Project objectives",
                "type": "Transformation",
                "urgency": "Medium",
                "sponsor": "Project Sponsor",
                "business_value": "Medium",
                "technical_complexity": "Medium",
                "resource_availability": "Medium",
                "timeline_pressure": "Medium",
                "total_score": 25
            }
        
        agents = self._create_agents(inputs)
        tasks = self._create_tasks(agents, inputs)
        
        # Create crew with COST OPTIMIZATION
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
        
        # Cost-optimized LLM configuration
        llm = ChatOpenAI(
            model=model,
            temperature=0.1,  # Low temperature for consistent, focused output
            max_tokens=800,   # Reduced from 1000 to save costs
            top_p=0.9,
            frequency_penalty=0.1,
            presence_penalty=0.1
        )
        
        return Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=False,  # Disable verbose to reduce token usage
            memory=False,   # Disable memory to save costs
            max_rpm=5,      # Reduced from 10 to limit API calls
            max_iter=2,     # Reduced from 3 to limit iterations
            process=Process.sequential,
            manager_llm=llm
        )

    def get_cost_estimate(self) -> dict:
        """Get current cost estimate"""
        return cost_estimator.get_estimate()

    def print_cost_estimate(self):
        """Print current cost estimate"""
        cost_estimator.print_estimate()
