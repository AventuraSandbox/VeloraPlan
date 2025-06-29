# Setup Guide

## Environment Configuration

This project uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

### 1. Create .env File

Create a file named `.env` in the project root directory:

```bash
# On Windows (PowerShell)
New-Item -Path ".env" -ItemType File

# On macOS/Linux
touch .env
```

### 2. Required Environment Variables

Add the following content to your `.env` file:

```bash
# =============================================================================
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
```

### 3. Get an OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the generated API key
5. Replace `your-openai-api-key-here` in your `.env` file

### 4. Set Environment Variable (Alternative Method)

If you prefer to set the environment variable directly instead of using a `.env` file:

#### On Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
$env:OPENAI_MODEL="gpt-4.1-nano"
```

#### On Windows (Command Prompt):
```cmd
set OPENAI_API_KEY=your-api-key-here
set OPENAI_MODEL=gpt-4.1-nano
```

#### On macOS/Linux:
```bash
export OPENAI_API_KEY="your-api-key-here"
export OPENAI_MODEL=gpt-4.1-nano
```

### 5. Verify Setup

Run the test script to verify your configuration:

```bash
python test_openai.py
```

You should see:
```
✅ OpenAI API key found
✅ OpenAI LLM object created successfully!
🤖 Model: gpt-4.1-nano (Cost Optimized)
💰 Cost-saving features: temperature=0.1, max_tokens=1000
✅ Test response: [response text]...
💰 Estimated cost for this test: ~$0.0001
```

### 6. Run the Project

Once configured, you can run the project:

```bash
crewai run
```

## Environment Variable Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | ❌ No | gpt-4.1-nano | OpenAI model to use |
| `OPENAI_MAX_TOKENS` | ❌ No | 1000 | Maximum response length |
| `OPENAI_TEMPERATURE` | ❌ No | 0.1 | Response creativity (0-1) |
| `OPENAI_TOP_P` | ❌ No | 0.9 | Response diversity (0-1) |
| `PROJECT_TYPE` | ❌ No | AI/ML | Type of project |
| `PROJECT_OBJECTIVES` | ❌ No | digital transformation | Project objectives |
| `INDUSTRY` | ❌ No | technology | Industry context |
| `VERBOSE` | ❌ No | false | Enable verbose output |
| `OUTPUT_DIR` | ❌ No | outputs | Output directory |
| `ENABLE_CACHING` | ❌ No | true | Enable result caching |
| `ENABLE_COST_MONITORING` | ❌ No | true | Show cost estimates |

## Cost Optimization Settings

### For Maximum Cost Savings:
```bash
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.1
OPENAI_MODEL=gpt-4.1-nano
VERBOSE=false
ENABLE_CACHING=true
```

### For Better Quality (Higher Cost):
```bash
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.3
OPENAI_MODEL=gpt-4.1-nano
VERBOSE=true
```

## Troubleshooting

### API Key Not Found
- Make sure you've set the environment variable correctly
- Check that the variable name is exactly `OPENAI_API_KEY`
- Restart your terminal after setting the variable
- Verify the `.env` file is in the project root directory

### API Call Failed
- Verify your OpenAI account has sufficient credits
- Check that your API key is valid and active
- Ensure you're not hitting rate limits
- Try reducing `OPENAI_MAX_TOKENS` if you're hitting limits

### Model Not Available
- The project uses `gpt-4.1-nano` by default
- Ensure your OpenAI account has access to the selected model
- You can change the model in the `.env` file if needed

### High Costs
- Reduce `OPENAI_MAX_TOKENS` to 500-1000
- Set `OPENAI_TEMPERATURE` to 0.1
- Set `VERBOSE` to false
- Enable caching with `ENABLE_CACHING=true` 