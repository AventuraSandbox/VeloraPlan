#!/usr/bin/env python3
"""
Simple test script to verify Gantt chart generation
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from veloraplan.crew import MermaidGanttGeneratorTool

def test_gantt_generation():
    """Test the Gantt chart generation tool"""
    tool = MermaidGanttGeneratorTool()
    
    # Test with realistic task data
    test_tasks = [
        "Requirements Analysis:1:3",
        "System Design:4:5", 
        "Development:9:10",
        "Testing:19:5",
        "Deployment:24:2"
    ]
    
    try:
        result = tool._run(test_tasks)
        print("✅ Gantt chart generation successful!")
        print("\nGenerated Gantt Chart:")
        print("=" * 50)
        print(result)
        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Gantt chart generation failed: {e}")
        return False

if __name__ == "__main__":
    test_gantt_generation() 