# Veloraplan Crew

Welcome to the Veloraplan Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## 🚀 Cost Optimized

This project has been **optimized for cost efficiency** with OpenAI GPT-4.1-nano:
- **Expected cost per run**: $0.03 - $0.10 (typical)
- **Built-in cost monitoring**: Real-time cost estimation
- **Optimized parameters**: temperature=0.1, max_tokens=1000
- **Concise prompts**: Reduced token usage while maintaining quality

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Environment Setup

**Option 1: Automatic Setup (Recommended)**
```bash
python create_env.py
```
This will create a `.env` file with all the necessary configuration.

**Option 2: Manual Setup**
Create a `.env` file in the project root and add your configuration. See [SETUP.md](SETUP.md) for detailed instructions.

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

1. Edit the `.env` file created by the setup script
2. Replace `your-openai-api-key-here` with your actual OpenAI API key
3. Set `OPENAI_MODEL=gpt-4.1-nano`
4. Adjust other settings as needed

- Modify `src/veloraplan/config/agents.yaml` to define your agents
- Modify `src/veloraplan/config/tasks.yaml` to define your tasks
- Modify `src/veloraplan/crew.py` to add your own logic, tools and specific args
- Modify `src/veloraplan/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the veloraplan Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The veloraplan Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Model Configuration

This project uses **gpt-4.1-nano** as the underlying language model with cost optimization:

### Cost Optimization Features
- **Temperature**: 0.1 (focused responses)
- **Max Tokens**: 1000 (limited response length)
- **Verbose**: false (reduced logging)
- **Concise Prompts**: Optimized agent and task descriptions

### Cost Monitoring
The project includes built-in cost estimation that displays:
- Input/output token counts
- Estimated cost in USD
- Real-time monitoring during execution

Make sure you have:
1. A valid OpenAI API key
2. Sufficient credits in your OpenAI account
3. The API key set as an environment variable: `OPENAI_API_KEY`
4. The model set as: `OPENAI_MODEL=gpt-4.1-nano`

## Cost Management

### Expected Costs
- **Typical run**: $0.03 - $0.10 (with gpt-4.1-nano)
- **Input tokens**: ~2,000 - 5,000
- **Output tokens**: ~1,000 - 3,000

> **Note:** GPT-4.1-nano is significantly more cost-effective than previous GPT-4 models, with similar or better performance for most project management and planning tasks.

### Cost Optimization Tips
1. **Test first**: Run `python test_openai.py` to verify setup
2. **Monitor usage**: Check cost estimates after each run
3. **Use caching**: The project includes built-in caching
4. **Batch operations**: Run multiple projects sequentially

For detailed cost optimization strategies, see [COST_OPTIMIZATION.md](COST_OPTIMIZATION.md).

## Support

For support, questions, or feedback regarding the Veloraplan Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
