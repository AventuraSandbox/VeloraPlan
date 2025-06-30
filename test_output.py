#!/usr/bin/env python
from datetime import datetime
import os

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

# Test the function
test_output = """
# Project Charter: Test Project

## Executive Summary
This is a test project to verify output file creation.

## Project Objectives
- Test output generation
- Verify file creation

```mermaid
gantt
    title Test Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1
    Task 1 :done, task1, 2024-01-01, 5d
    Task 2 :done, task2, 2024-01-06, 3d
```

## Project Timeline
This project will run for 2 weeks.
"""

print("🧪 Testing output file creation...")
save_output_to_files(test_output)
print("✅ Test completed! Check the 'outputs' directory.") 