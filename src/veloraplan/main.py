#!/usr/bin/env python
# Author: Meltem Singh
# Contact: aventura.sandbox@gmail.com
#
# main.py for VeloraPlan - Workday ERP Implementation

import sys
import warnings
from datetime import datetime
import os
import json

# Suppress known warnings from crewai dependencies
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Import your crew configuration
from veloraplan.crew import Veloraplan
from veloraplan.project_loader import create_project_loader

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def save_output_to_files(output):
    """Save the crew output to files for easy viewing."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create output directory
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Convert output to string if it's not already
    output_str = str(output)
    
    # Save the full output
    with open(f"{output_dir}/crew_output_{timestamp}.md", "w", encoding="utf-8") as f:
        f.write(output_str)
    
    # Extract and save Gantt chart separately
    if "```mermaid" in output_str:
        start_idx = output_str.find("```mermaid")
        end_idx = output_str.find("```", start_idx + 10)
        if end_idx != -1:
            gantt_content = output_str[start_idx:end_idx + 3]
            with open(f"{output_dir}/gantt_chart_{timestamp}.md", "w", encoding="utf-8") as f:
                f.write(gantt_content)
            print(f"✅ Gantt chart saved to: {output_dir}/gantt_chart_{timestamp}.md")
    
    # Save project charter
    if "# Project Charter:" in output_str:
        charter_start = output_str.find("# Project Charter:")
        charter_end = output_str.find("## Project Timeline", charter_start)
        if charter_end == -1:
            charter_end = output_str.find("## Resource Allocation Plan", charter_start)
        if charter_end == -1:
            charter_end = len(output_str)
        
        charter_content = output_str[charter_start:charter_end].strip()
        with open(f"{output_dir}/project_charter_{timestamp}.md", "w", encoding="utf-8") as f:
            f.write(charter_content)
        print(f"✅ Project charter saved to: {output_dir}/project_charter_{timestamp}.md")
    
    print(f"✅ Full output saved to: {output_dir}/crew_output_{timestamp}.md")

def run():
    """
    Run the crew with OpenAI (Cost Optimized) using project configuration.
    """
    try:
        # Load project configuration
        project_loader = create_project_loader()
        config = project_loader.config
        
        print(f"🚀 Starting: {config.project_charter.title}")
        print(f"💰 Budget: ${config.project_charter.budget:,.0f} | 📅 {config.project_charter.start_date} to {config.project_charter.end_date}")
        print(f"🎯 {len(config.project_phases)} phases | ⚠️ {len(config.risks)} risks identified")
        
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")
        print(f"🤖 {model} | 💰 Cost optimized: max_tokens=800, max_iter=2, verbose=false")
        
        veloraplan = Veloraplan()
        crew = veloraplan.crew()
        
        # Run the crew
        result = crew.kickoff()
        
        # Save the output to files
        save_output_to_files(result)
        
        # Print cost estimate
        veloraplan.print_cost_estimate()

        # Automatically extract outputs after run
        try:
            import subprocess
            subprocess.run(["python", "extract_outputs.py"], check=True)
        except Exception as e:
            print(f"⚠️  Could not run extract_outputs.py automatically: {e}")
        
        print("\n" + "="*50)
        print("✅ CREW EXECUTION COMPLETED!")
        print("="*50)
        print("\n📁 Generated files in 'outputs/' directory:")
        print("- project_charter_*.md - Complete project charter")
        print("- gantt_chart_*.md - Enhanced timeline")
        print("- resource_allocation_*.md - Resource plan")
        print("- prioritization_analysis_*.md - Priority analysis")
        print("- risk_assessment_*.md - Risk register")
        print("- detailed_project_plan_*.md - Project plan")
        print(f"\n🤖 Powered by {model} (Cost Optimized)")
        
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    Usage: python main.py <n_iterations> <output_filename>
    """
    try:
        project_loader = create_project_loader()
        inputs = project_loader.get_crew_inputs()
        
        Veloraplan().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    Usage: python main.py <task_id>
    """
    try:
        Veloraplan().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    Usage: python main.py <n_iterations> <llm_model>
    """
    try:
        project_loader = create_project_loader()
        inputs = project_loader.get_crew_inputs()
        
        Veloraplan().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    run()
