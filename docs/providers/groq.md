# Groq Provider

Groq is an AI infrastructure company that provides fast inference for large language models. This provider allows Keep to use Groq's API for AI-driven tasks within workflows.

## Authentication

To connect Keep to Groq, you need a Groq Cloud API Key.
- **Api Key**: Your Groq API Key (generated at https://console.groq.com/keys).

## Functionality

The provider supports querying Large Language Models (LLMs) hosted by Groq.

### Actions

#### `query`
Sends a prompt to a Groq-hosted model and returns the response.

**Parameters:**
- `prompt` (required): The prompt to send to the model.
- `model` (optional): The Groq model to use (default: \"llama3-8b-8192\").
- `max_tokens` (optional): The maximum number of tokens to generate.
- `temperature` (optional): The sampling temperature to use.
