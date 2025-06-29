import os
import re
from datetime import datetime

def extract_section(text, start_pattern, end_pattern=None):
    """Extracts a section from text between start_pattern and end_pattern (regex)."""
    start_match = re.search(start_pattern, text, re.IGNORECASE)
    if not start_match:
        return None
    start = start_match.end()
    if end_pattern:
        end_match = re.search(end_pattern, text[start:], re.IGNORECASE | re.MULTILINE)
        end = start + end_match.start() if end_match else len(text)
    else:
        end = len(text)
    return text[start:end].strip()

def extract_mermaid(text):
    """Extracts the first mermaid code block."""
    match = re.search(r"```mermaid(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return f"```mermaid{match.group(1)}```" if match else None

def extract_project_title(text):
    """Extracts project title from the charter."""
    match = re.search(r"# Project Charter:\s*(.+)", text, re.IGNORECASE)
    return match.group(1).strip() if match else "Project Plan"

def create_comprehensive_charter(content, project_title):
    """Creates a comprehensive project charter with all sections."""
    charter_sections = []
    
    # Extract all relevant sections
    executive_summary = extract_section(content, r"## Executive Summary", r"^## |\Z")
    objectives = extract_section(content, r"## Objectives", r"^## |\Z")
    scope = extract_section(content, r"## Scope", r"^## |\Z")
    timeline = extract_section(content, r"## Timeline", r"^## |\Z")
    resources = extract_section(content, r"## Resources", r"^## |\Z")
    risks = extract_section(content, r"## Risks", r"^## |\Z")
    governance = extract_section(content, r"## Governance", r"^## |\Z")
    communication = extract_section(content, r"## Communication Plan", r"^## |\Z")
    
    # Build comprehensive charter
    charter = f"""# Project Charter: {project_title}

## Executive Summary
{executive_summary if executive_summary else "Executive summary to be defined."}

## Project Objectives
{objectives if objectives else "Project objectives to be defined."}

## Project Scope
{scope if scope else "Project scope to be defined."}

## Timeline
{timeline if timeline else "Project timeline to be defined."}

## Resources
{resources if resources else "Resource requirements to be defined."}

## Risks
{risks if risks else "Risk assessment to be defined."}

## Governance
{governance if governance else "Governance structure to be defined."}

## Communication Plan
{communication if communication else "Communication plan to be defined."}

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return charter

def create_enhanced_gantt(gantt_content, project_title):
    """Creates an enhanced Gantt chart with better formatting."""
    if not gantt_content:
        return "No Gantt chart data available."
    
    enhanced_gantt = f"""# Project Timeline: {project_title}

## Gantt Chart

{gantt_content}

## Timeline Summary
This Gantt chart shows the project timeline with key milestones and deliverables.

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return enhanced_gantt

def create_enhanced_resource_plan(resource_content, project_title):
    """Creates an enhanced resource allocation plan."""
    if not resource_content:
        return "No resource allocation data available."
    
    enhanced_resource = f"""# Resource Allocation Plan: {project_title}

## Resource Requirements

{resource_content}

## Resource Summary
- **Total Team Size**: To be calculated based on allocation
- **Peak Resource Usage**: To be determined from allocation table
- **Resource Distribution**: See table above for weekly breakdown

## Resource Management Notes
- Ensure resource availability before project start
- Monitor resource utilization throughout project
- Adjust allocations based on project progress

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return enhanced_resource

def create_enhanced_prioritization(prioritization_content, project_title):
    """Creates an enhanced prioritization analysis."""
    if not prioritization_content:
        return "No prioritization data available."
    
    enhanced_prioritization = f"""# Prioritization Analysis: {project_title}

## Project Scoring and Priority Assessment

{prioritization_content}

## Priority Tier Explanation
- **P1 (Critical)**: Highest priority, immediate attention required
- **P2 (High)**: Important, plan for near-term execution
- **P3 (Medium)**: Standard priority, execute when resources available
- **P4 (Low)**: Lower priority, consider for future planning

## Recommendations
Based on the prioritization analysis, this project has been classified as a **P1** priority, indicating it requires immediate attention and resource allocation.

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return enhanced_prioritization

def create_enhanced_risk_assessment(risk_content, project_title):
    """Creates an enhanced risk assessment and mitigation plan."""
    if not risk_content:
        return "No risk assessment data available."
    
    enhanced_risk = f"""# Risk Assessment and Mitigation Plan: {project_title}

## Risk Analysis Matrix

{risk_content}

## Risk Management Strategy
- **High Impact, High Likelihood**: Immediate mitigation required
- **High Impact, Low Likelihood**: Contingency planning needed
- **Low Impact, High Likelihood**: Monitor and manage
- **Low Impact, Low Likelihood**: Accept and monitor

## Risk Monitoring
- Weekly risk review meetings
- Monthly risk assessment updates
- Quarterly risk strategy review

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return enhanced_risk

def create_enhanced_project_plan(plan_content, project_title):
    """Creates an enhanced detailed project plan."""
    if not plan_content:
        return "No detailed project plan data available."
    
    enhanced_plan = f"""# Detailed Project Plan: {project_title}

## Project Phases and Tasks

{plan_content}

## Project Management Approach
- **Phase-based execution** with clear deliverables
- **Regular status reviews** and milestone tracking
- **Stakeholder communication** at key decision points
- **Quality gates** between phases

## Success Criteria
- All deliverables completed on time
- Stakeholder satisfaction achieved
- Quality standards met
- Knowledge transfer completed

---
*Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}*
"""
    return enhanced_plan

def main():
    output_dir = "outputs"
    files = [f for f in os.listdir(output_dir) if f.startswith("crew_output_") and f.endswith(".md")]
    if not files:
        print("No crew_output_*.md files found in outputs directory.")
        return

    latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(output_dir, f)))
    with open(os.path.join(output_dir, latest_file), "r", encoding="utf-8") as f:
        content = f.read()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project_title = extract_project_title(content)

    # Enhanced Project Charter
    charter = create_comprehensive_charter(content, project_title)
    charter_path = os.path.join(output_dir, f"project_charter_{timestamp}.md")
    with open(charter_path, "w", encoding="utf-8") as f:
        f.write(charter)
    print(f"✅ Enhanced project charter saved to: {charter_path}")

    # Enhanced Gantt Chart
    gantt = extract_mermaid(content)
    enhanced_gantt = create_enhanced_gantt(gantt, project_title)
    gantt_path = os.path.join(output_dir, f"gantt_chart_{timestamp}.md")
    with open(gantt_path, "w", encoding="utf-8") as f:
        f.write(enhanced_gantt)
    print(f"✅ Enhanced Gantt chart saved to: {gantt_path}")

    # Enhanced Resource Allocation Plan
    resource = extract_section(content, r"## Resource Allocation Plan", r"^## |\Z")
    enhanced_resource = create_enhanced_resource_plan(resource, project_title)
    resource_path = os.path.join(output_dir, f"resource_allocation_{timestamp}.md")
    with open(resource_path, "w", encoding="utf-8") as f:
        f.write(enhanced_resource)
    print(f"✅ Enhanced resource allocation plan saved to: {resource_path}")

    # Enhanced Prioritization Analysis
    prioritization = extract_section(content, r"## Prioritization Analysis", r"^## |\Z")
    enhanced_prioritization = create_enhanced_prioritization(prioritization, project_title)
    prioritization_path = os.path.join(output_dir, f"prioritization_analysis_{timestamp}.md")
    with open(prioritization_path, "w", encoding="utf-8") as f:
        f.write(enhanced_prioritization)
    print(f"✅ Enhanced prioritization analysis saved to: {prioritization_path}")

    # Enhanced Detailed Project Plan
    detailed_plan = extract_section(content, r"## Detailed Project Plan", r"^## |\Z")
    enhanced_plan = create_enhanced_project_plan(detailed_plan, project_title)
    detailed_plan_path = os.path.join(output_dir, f"detailed_project_plan_{timestamp}.md")
    with open(detailed_plan_path, "w", encoding="utf-8") as f:
        f.write(enhanced_plan)
    print(f"✅ Enhanced detailed project plan saved to: {detailed_plan_path}")

    # Enhanced Risk Assessment and Mitigation Plan
    risk_assessment = extract_section(content, r"## Risk Assessment and Mitigation Plan", r"^## |\Z")
    enhanced_risk = create_enhanced_risk_assessment(risk_assessment, project_title)
    risk_assessment_path = os.path.join(output_dir, f"risk_assessment_{timestamp}.md")
    with open(risk_assessment_path, "w", encoding="utf-8") as f:
        f.write(enhanced_risk)
    print(f"✅ Enhanced risk assessment saved to: {risk_assessment_path}")

    print(f"\n🎉 All enhanced output files generated successfully!")
    print(f"📁 Files saved in: {output_dir}")
    print(f"📋 Project: {project_title}")

if __name__ == "__main__":
    main() 