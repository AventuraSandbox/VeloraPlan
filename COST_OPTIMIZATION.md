# Cost Optimization Guide

## Overview

This project has been optimized to minimize OpenAI API costs while maintaining quality. Here's how we've reduced costs and how you can further optimize:

## Built-in Cost Optimizations

### 1. LLM Configuration
- **Temperature**: 0.1 (lower = more focused, fewer tokens)
- **Max Tokens**: 1000 (limits response length)
- **Top P**: 0.9 (reduces randomness)
- **Frequency/Presence Penalty**: 0.1 (encourages concise responses)

### 2. Agent Optimization
- **Verbose**: false (reduces logging output)
- **Concise Descriptions**: Shortened role/goal/backstory text
- **Focused Tasks**: Streamlined task descriptions

### 3. Task Optimization
- **Condensed Descriptions**: Removed redundant text
- **Clear Output Formats**: Structured JSON responses
- **Efficient Prompts**: Reduced token usage in prompts

## Expected Costs

### Per Run Estimates
- **Typical Run**: $0.01 - $0.05
- **Input Tokens**: ~2,000 - 5,000
- **Output Tokens**: ~1,000 - 3,000

### Cost Breakdown
- **Input**: $0.0005 per 1K tokens
- **Output**: $0.0015 per 1K tokens
- **Total**: ~$0.0025 - $0.0125 per run

## Further Cost Optimization Tips

### 1. Environment Variables
```bash
# Set a lower max_tokens if needed
export OPENAI_MAX_TOKENS=500

# Use a different model for testing
export OPENAI_MODEL=gpt-4.1-nano-16k  # For longer contexts
```

### 2. Customize Agent Descriptions
Edit `src/veloraplan/config/agents.yaml` to make descriptions even more concise:
```yaml
project_planner_agent:
  role: "Project Manager"
  goal: "Create project plans for {project_type} projects."
  backstory: "Experienced PM in {project_type} and {industry}."
```

### 3. Simplify Task Descriptions
Edit `src/veloraplan/config/tasks.yaml` to reduce prompt length:
```yaml
project_planning_task:
  description: "Create project plan with scope, timeline, resources."
  expected_output: "JSON with project details."
```

### 4. Use Caching
The project already includes caching for:
- Project intake forms
- Tool results
- Repeated queries

### 5. Batch Processing
For multiple projects, consider:
- Running them sequentially to reuse context
- Using the same crew instance
- Sharing common data between runs

## Monitoring Costs

### Real-time Monitoring
The project includes built-in cost estimation:
```python
from veloraplan.crew import Veloraplan

veloraplan = Veloraplan()
crew = veloraplan.crew()
result = crew.kickoff(inputs=inputs)

# Get cost estimate
cost = veloraplan.get_cost_estimate()
print(f"Cost: ${cost['estimated_cost_usd']}")
```

### OpenAI Dashboard
Monitor usage at: https://platform.openai.com/usage

## Advanced Optimization

### 1. Use Different Models
```python
# For testing (cheaper)
llm = LLM(provider="openai", model="gpt-4.1-nano", max_tokens=500)

# For production (more capable)
llm = LLM(provider="openai", model="gpt-4", max_tokens=1000)
```

### 2. Implement Retry Logic
```python
# Add retry logic for failed API calls
import time
from openai import RateLimitError

def safe_api_call(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
```

### 3. Token Counting
```python
import tiktoken

def count_tokens(text: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-4.1-nano")
    return len(encoding.encode(text))
```

## Cost Comparison

| Configuration | Estimated Cost | Quality | Use Case |
|---------------|----------------|---------|----------|
| Current (Optimized) | $0.01-0.05 | High | Production |
| Minimal | $0.005-0.02 | Medium | Testing |
| Full Quality | $0.05-0.15 | Very High | Complex Projects |

## Best Practices

1. **Start Small**: Test with minimal configurations first
2. **Monitor Usage**: Check costs regularly
3. **Cache Results**: Reuse outputs when possible
4. **Batch Requests**: Group related operations
5. **Use Appropriate Models**: Choose based on complexity needs

## Troubleshooting High Costs

### If costs are higher than expected:
1. Check for infinite loops in agent interactions
2. Verify max_tokens is set appropriately
3. Review agent descriptions for verbosity
4. Ensure caching is working properly
5. Monitor for repeated API calls

### Common Issues:
- **Verbose agents**: Set `verbose: false`
- **Long prompts**: Shorten task descriptions
- **Repeated calls**: Check for caching issues
- **High token limits**: Reduce max_tokens 