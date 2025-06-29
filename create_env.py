#!/usr/bin/env python3
"""
Helper script to create a .env file for VeloraPlan
"""
import os
from pathlib import Path

def create_env_file():
    """Create a .env file with default configuration"""
    
    env_content = """# =============================================================================
# VeloraPlan Environment Configuration
# =============================================================================

# OpenAI Configuration (REQUIRED)
# Get your API key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your-openai-api-key-here

# Optional: OpenAI Model Configuration
# Default: gpt-4.1-nano (cost optimized)
OPENAI_MODEL=gpt-4.1-nano

# Optional: Cost Optimization Settings
# Reduce these values to save more money (but may affect quality)
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.1
OPENAI_TOP_P=0.9
OPENAI_FREQUENCY_PENALTY=0.1
OPENAI_PRESENCE_PENALTY=0.1

# Project Configuration
PROJECT_TYPE=AI/ML
PROJECT_OBJECTIVES=digital transformation
INDUSTRY=technology

# Optional: Debug and Logging
# Set to true for verbose output (increases costs)
VERBOSE=false

# Optional: Output Directory
# Where generated files will be saved
OUTPUT_DIR=outputs

# Optional: Cache Settings
# Enable/disable caching to save API calls
ENABLE_CACHING=true

# Optional: Cost Monitoring
# Enable/disable cost estimation display
ENABLE_COST_MONITORING=true

# =============================================================================
# Next Steps:
# =============================================================================
# 1. Replace 'your-openai-api-key-here' with your actual OpenAI API key
# 2. Adjust other settings as needed
# 3. Run: crewai run
# =============================================================================
"""
    
    env_path = Path(".env")
    
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("❌ .env file creation cancelled")
            return False
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print("📝 Next steps:")
        print("   1. Edit .env file and add your OpenAI API key")
        print("   2. Run: python test_openai.py")
        print("   3. Run: crewai run")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def main():
    print("🚀 VeloraPlan .env File Creator")
    print("=" * 40)
    
    success = create_env_file()
    
    if success:
        print("\n💡 For more information, see SETUP.md")
    else:
        print("\n💡 You can manually create a .env file following the instructions in SETUP.md")

if __name__ == "__main__":
    main() 