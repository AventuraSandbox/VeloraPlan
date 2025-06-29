import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional
from veloraplan.models import ProjectConfig, ProjectStatus, Deliverable

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / 'config' / 'project_config.yaml'

class ProjectLoader:
    """Loads and manages project configuration for CrewAI system"""
    
    def __init__(self, config_path: str = None):
        self.config_path = str(DEFAULT_CONFIG_PATH if config_path is None else config_path)
        self.config: Optional[ProjectConfig] = None
        self.status: Optional[ProjectStatus] = None
        self.deliverables: Dict[str, Deliverable] = {}
        
    def load_config(self) -> ProjectConfig:
        """Load project configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
        
        self.config = ProjectConfig(**data)
        return self.config
    
    def initialize_deliverables(self) -> Dict[str, Deliverable]:
        """Initialize deliverables from project phases"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        self.deliverables = {}
        for phase in self.config.project_phases:
            for deliverable_name in phase.deliverables:
                deliverable = Deliverable(
                    name=deliverable_name,
                    phase=phase.name,
                    due_date=None,  # Will be calculated based on phase timeline
                    owner=None,     # Will be assigned based on resource allocation
                    dependencies=[],
                    notes=f"Deliverable from {phase.name} phase"
                )
                self.deliverables[deliverable_name] = deliverable
        
        return self.deliverables
    
    def initialize_status(self) -> ProjectStatus:
        """Initialize project status"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        self.status = ProjectStatus(
            current_phase=self.config.project_phases[0].name,
            phase_progress=0.0,
            overall_progress=0.0,
            budget_consumed=0.0,
            risks_identified=len(self.config.risks),
            risks_mitigated=0
        )
        
        return self.status
    
    def get_crew_inputs(self) -> Dict[str, Any]:
        """Get inputs for CrewAI system"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        return {
            "project_id": f"PRJ-{self.config.project_charter.title.replace(' ', '-')}",
            "current_year": "2025",
            "project_title": self.config.project_charter.title,
            "objectives": "\n".join([f"- {goal}" for goal in self.config.project_charter.goals]),
            "type": "AI/ML Transformation",
            "urgency": "High",
            "sponsor": self.config.project_charter.sponsor,
            "business_value": "High",
            "technical_complexity": "High",
            "resource_availability": "Medium",
            "timeline_pressure": "High",
            "total_score": sum(item.score for item in self.config.prioritization_analysis),
            "budget": self.config.project_charter.budget,
            "start_date": self.config.project_charter.start_date,
            "end_date": self.config.project_charter.end_date,
            "business_need": self.config.project_charter.business_need,
            "scope_includes": "\n".join([f"- {item}" for item in self.config.project_charter.scope.includes]),
            "scope_excludes": "\n".join([f"- {item}" for item in self.config.project_charter.scope.excludes]),
            "assumptions": "\n".join([f"- {assumption}" for assumption in self.config.project_charter.assumptions]),
            "constraints": "\n".join([f"- {constraint}" for constraint in self.config.project_charter.constraints]),
            "stakeholders": "\n".join([f"- {stakeholder}" for stakeholder in self.config.project_charter.stakeholders])
        }
    
    def get_phase_info(self) -> Dict[str, Any]:
        """Get phase information for task generation"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        phases_info = {}
        for phase in self.config.project_phases:
            phases_info[phase.name] = {
                "duration_days": phase.duration_days,
                "deliverables": phase.deliverables,
                "duration_weeks": phase.duration_days // 7
            }
        
        return phases_info
    
    def get_risk_summary(self) -> str:
        """Get formatted risk summary"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        risk_summary = "## Risk Register\n\n"
        for risk in self.config.risks:
            risk_summary += f"**{risk.id}: {risk.description}**\n"
            risk_summary += f"- Likelihood: {risk.likelihood}\n"
            risk_summary += f"- Impact: {risk.impact}\n"
            risk_summary += f"- Mitigation: {risk.mitigation}\n\n"
        
        return risk_summary
    
    def get_prioritization_summary(self) -> str:
        """Get formatted prioritization summary"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        # Sort by score descending
        sorted_items = sorted(self.config.prioritization_analysis, key=lambda x: x.score, reverse=True)
        
        prioritization_summary = "## Prioritization Analysis\n\n"
        prioritization_summary += "| Item | Impact | Urgency | Complexity | Score |\n"
        prioritization_summary += "|------|--------|---------|------------|-------|\n"
        
        for item in sorted_items:
            prioritization_summary += f"| {item.item} | {item.impact} | {item.urgency} | {item.complexity} | {item.score} |\n"
        
        return prioritization_summary
    
    def get_resource_summary(self) -> str:
        """Get formatted resource allocation summary"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        resource_summary = "## Resource Allocation\n\n"
        resource_summary += "| Role | Total FTE | Peak FTE |\n"
        resource_summary += "|------|-----------|----------|\n"
        
        for resource in self.config.resource_allocation:
            total_fte = sum(resource.allocation)
            peak_fte = max(resource.allocation)
            resource_summary += f"| {resource.role} | {total_fte} | {peak_fte} |\n"
        
        return resource_summary
    
    def get_financial_summary(self) -> str:
        """Get formatted financial summary"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        financial_summary = "## Financial Summary\n\n"
        financial_summary += "| Category | Planned | Actual | Variance |\n"
        financial_summary += "|----------|---------|--------|----------|\n"
        
        total_planned = 0
        total_actual = 0
        
        for financial in self.config.financials:
            planned = financial.planned
            actual = financial.actual or 0
            variance = financial.variance or (actual - planned)
            
            total_planned += planned
            total_actual += actual
            
            financial_summary += f"| {financial.category} | ${planned:,.0f} | ${actual:,.0f} | ${variance:,.0f} |\n"
        
        financial_summary += f"| **Total** | **${total_planned:,.0f}** | **${total_actual:,.0f}** | **${total_actual - total_planned:,.0f}** |\n"
        
        return financial_summary
    
    def get_stakeholder_communication_plan(self) -> str:
        """Get formatted stakeholder communication plan"""
        if not self.config:
            raise ValueError("Configuration must be loaded first")
        
        comm_plan = "## Stakeholder Communication Plan\n\n"
        comm_plan += "| Stakeholder | Needs | Frequency | Channel |\n"
        comm_plan += "|-------------|-------|-----------|---------|\n"
        
        for comm in self.config.stakeholder_communications:
            comm_plan += f"| {comm.stakeholder} | {comm.needs} | {comm.frequency} | {comm.channel} |\n"
        
        return comm_plan

def load_project_config(config_path: str = None) -> ProjectConfig:
    """Convenience function to load project configuration"""
    loader = ProjectLoader(config_path)
    return loader.load_config()

def create_project_loader(config_path: str = None) -> ProjectLoader:
    """Create and initialize a project loader"""
    loader = ProjectLoader(config_path)
    loader.load_config()
    loader.initialize_deliverables()
    loader.initialize_status()
    return loader 