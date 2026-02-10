# OpenClaw + Purdue GenAI Studio Integration Guide

This guide explains how to integrate OpenClaw agents with Purdue GenAI Studio API as the LLM backend.

## Overview

This integration allows you to:
- Use Purdue GenAI Studio's on-premises LLM models with OpenClaw
- Maintain conversation history across interactions
- Monitor agent performance with AgentOps
- Leverage multiple available models (LLaMA, DeepSeek, Qwen, etc.)

## Architecture

`
OpenClaw Agent â†’ Purdue GenAI Provider â†’ Purdue GenAI Studio API
                      â†“
                 AgentOps Monitoring
`

## Setup

### 1. Prerequisites

`ash
pip install requests python-dotenv
`

Optional (for monitoring):
`ash
pip install agentops
`

### 2. Environment Configuration

Add to your .env file:

`env
# Purdue GenAI Studio
PURDUE_GENAI_API_KEY=your_api_key_here
PURDUE_GENAI_BASE_URL=https://genai.rcac.purdue.edu/api/v1
PURDUE_GENAI_MODEL=llama3.2:latest

# AgentOps (optional)
AGENTOPS_API_KEY=your_agentops_key_here
`

### 3. Basic Usage

`python
from openclaw_genai_integration import PurdueGenAIProvider, OpenClawAgent
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize GenAI provider
genai_provider = PurdueGenAIProvider(
    api_key=os.getenv("PURDUE_GENAI_API_KEY"),
    model="llama3.2:latest"
)

# Create OpenClaw agent
agent = OpenClawAgent(
    name="My Agent",
    genai_provider=genai_provider,
    system_prompt="You are a helpful assistant."
)

# Use the agent
response = agent.process("What is machine learning?")
print(response)
`

## Features

### 1. Conversation History

The agent maintains conversation history automatically:

`python
agent.process("What is AI?")
agent.process("How does it work?")  # Remembers previous context
`

### 2. Multiple Models

Switch between different models:

`python
# Use different model
genai_provider = PurdueGenAIProvider(
    api_key=api_key,
    model="deepseek-r1:7b"  # Reasoning model
)
`

### 3. Custom Parameters

Control generation parameters:

`python
response = agent.process(
    "Explain quantum computing",
    max_tokens=500,
    temperature=0.8  # More creative responses
)
`

### 4. AgentOps Monitoring

Monitor your agents with AgentOps:

`python
import agentops
agentops.init(os.getenv("AGENTOPS_API_KEY"))

# Your agent code here
agent.process("Hello!")

agentops.end_session("Success")
`

## Available Models

List all available models:

`python
models = genai_provider.list_models()
print(f"Available models: {models}")
`

Popular models:
- llama3.2:latest - General purpose
- deepseek-r1:7b - Reasoning model
- qwen3:8b - Qwen 3 model
- mistral:latest - Mistral model
- codellama:latest - Code-focused

## Example: Research Assistant

`python
agent = OpenClawAgent(
    name="Research Assistant",
    genai_provider=genai_provider,
    system_prompt="You are a research assistant. Provide accurate, well-sourced information."
)

# Research questions
response1 = agent.process("What are the latest developments in AI?")
response2 = agent.process("How do transformers work?")
response3 = agent.process("Compare different AI architectures.")
`

## Example: Code Assistant

`python
# Use code-focused model
code_provider = PurdueGenAIProvider(
    api_key=api_key,
    model="codellama:latest"
)

code_agent = OpenClawAgent(
    name="Code Assistant",
    genai_provider=code_provider,
    system_prompt="You are a coding assistant. Write clean, efficient code."
)

code = code_agent.process("Write a Python function to sort a list")
`

## Error Handling

`python
try:
    response = agent.process("Your question")
except Exception as e:
    print(f"Error: {e}")
    # Handle error appropriately
`

## Best Practices

1. **Reset conversations** when starting new topics:
   `python
   agent.reset_conversation()
   `

2. **Monitor token usage** to stay within limits:
   `python
   result = genai_provider.chat_completion(messages, max_tokens=500)
   tokens_used = result["usage"]["total_tokens"]
   `

3. **Use appropriate models** for different tasks:
   - General: llama3.2:latest
   - Reasoning: deepseek-r1:7b or deepseek-r1:14b
   - Code: codellama:latest
   - Vision: llava:latest

4. **Set system prompts** to guide agent behavior:
   `python
   agent = OpenClawAgent(
       name="Specialist",
       genai_provider=provider,
       system_prompt="You are an expert in [domain]. Provide detailed explanations."
   )
   `

## Troubleshooting

### API Connection Issues
- Verify your API key is correct
- Check network connectivity
- Ensure base URL is correct: https://genai.rcac.purdue.edu/api/v1

### Model Not Found
- List available models: genai_provider.list_models()
- Verify model name is exact (case-sensitive)

### Token Limits
- Reduce max_tokens parameter
- Clear conversation history periodically
- Use gent.reset_conversation()

## See Also

- [Purdue GenAI Studio Documentation](GENAI_CONNECTION.md)
- [OpenClaw Installation Guide](OPENCLAW_INSTALLATION.md)
- [Example Integration](examples/openclaw_genai_integration.py)
