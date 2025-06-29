#!/usr/bin/env python3
"""
Convert Mermaid Gantt charts to PNG images
"""
import os
import glob
import requests
import base64
from pathlib import Path

def convert_mermaid_to_png(mermaid_content, output_path):
    """Convert Mermaid content to PNG using mermaid.ink API"""
    try:
        # Encode the mermaid content
        encoded = base64.b64encode(mermaid_content.encode()).decode()
        
        # Use mermaid.ink API
        url = f"https://mermaid.ink/img/{encoded}?type=png"
        
        # Download the image
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the image
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Converted to PNG: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error converting to PNG: {e}")
        return False

def extract_mermaid_from_file(file_path):
    """Extract Mermaid content from markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find mermaid block
        start = content.find('```mermaid')
        if start == -1:
            return None
        
        start = content.find('\n', start) + 1
        end = content.find('```', start)
        
        if end == -1:
            return None
        
        return content[start:end].strip()
        
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return None

def main():
    """Convert all Gantt chart files to PNG"""
    # Find all gantt chart files
    gantt_files = glob.glob("outputs/gantt_chart_*.md")
    
    if not gantt_files:
        print("❌ No Gantt chart files found in outputs/ directory")
        return
    
    print(f"📊 Found {len(gantt_files)} Gantt chart files")
    
    for file_path in gantt_files:
        print(f"\n🔄 Processing: {file_path}")
        
        # Extract mermaid content
        mermaid_content = extract_mermaid_from_file(file_path)
        if not mermaid_content:
            print(f"❌ No Mermaid content found in {file_path}")
            continue
        
        # Create output path
        output_path = file_path.replace('.md', '.png')
        
        # Convert to PNG
        convert_mermaid_to_png(mermaid_content, output_path)

if __name__ == "__main__":
    main() 