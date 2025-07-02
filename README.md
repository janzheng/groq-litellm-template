# Groq + LiteLLM Universal API Proxy

[LiteLLM](https://docs.litellm.ai/docs/) provides a simple python-based framework with features to help productionize your application infrastructure, including:

- Cost Management: Track spending, set budgets, and implement rate limiting for optimal resource utilization
- Smart Caching: Cache frequent responses to reduce API calls while maintaining Groq's speed advantage
- Spend Tracking: Track spend for individual API keys, users, and teams


This example shows a production-ready FastAPI proxy server that provides OpenAI-compatible endpoints powered by Groq's fast inference through LiteLLM. Use this template to centralize all your AI API calls through one server, enabling unified usage tracking, budget management, and cost optimization across your entire organization.

## Overview

This application demonstrates how to create a centralized AI API gateway using LiteLLM and Groq API. Built as a complete, end-to-end template that you can fork, customize, and deploy to manage all your organization's AI API usage from one place.

**Key Features:**
- OpenAI-compatible API endpoints that work with any OpenAI client
- FastAPI proxy server with automatic request/response validation
- Direct LiteLLM integration examples for simple use cases
- Centralized API gateway for tracking usage, spending, and implementing budgets
- Production-ready with proper error handling and logging
- Sub-second response times and efficient request handling powered by Groq

**What You'll Learn:**
This template shows you how to build a centralized AI API gateway that gives you complete visibility and control over your organization's AI usage. You can track spending, implement budgets, cache responses for cost savings, and maintain OpenAI compatibility while leveraging Groq's speed advantages.

## Architecture

**Tech Stack:**
- **Backend Framework:** FastAPI with Pydantic validation
- **LLM Integration:** LiteLLM for universal provider support
- **AI Infrastructure:** Groq API for fast inference
- **HTTP Client:** Requests library for testing
- **Runtime:** Python 3.12+ with async/await support

**API Flow:**
- **Client** → Makes OpenAI-formatted request → **Your FastAPI Gateway** → **LiteLLM (with tracking)** → **Groq API**

## Quick Start

### Prerequisites
- Python 3.12+ and [uv](https://docs.astral.sh/uv/) package manager
- Groq API key ([Create a free GroqCloud account and generate an API key here](https://console.groq.com/keys))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/janzheng/groq-litellm-template
   cd groq-litellm-template/groq-litelllm
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file with your API key
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Test direct LiteLLM usage**
   ```bash
   uv run main.py
   ```

5. **Start the proxy server**
   ```bash
   uv run server.py
   ```

6. **Test the proxy server (in another terminal)**
   ```bash
   uv run client_example.py
   ```

## Examples

### 1. Direct LiteLLM Usage

**File:** `main.py` | **Command:** `uv run main.py`

The simplest way to use LiteLLM with Groq - demonstrates direct integration:

```python
import litellm

response = litellm.completion(
    model="groq/llama-3.3-70b-versatile", 
    messages=[{"role": "user", "content": "hello from litellm"}]
)
```

### 2. FastAPI Proxy Server

**File:** `server.py` | **Command:** `uv run server.py`

A production-ready proxy server that provides OpenAI-compatible endpoints:

**Available Endpoints:**
- `GET /` - Health check
- `GET /v1/models` - List available models (OpenAI-compatible)
- `POST /v1/chat/completions` - Chat completions (OpenAI-compatible)
- `POST /chat/completions` - Simplified endpoint without /v1 prefix

**Features:**
- Automatic request/response validation with Pydantic
- OpenAI-compatible API format
- Support for all OpenAI parameters (temperature, max_tokens, etc.)
- Proper error handling and HTTP status codes
- Configurable via environment variables

### 3. Client Examples

**File:** `client_example.py` | **Command:** `uv run client_example.py`

Comprehensive testing examples showing three different ways to use the proxy:

1. **Direct HTTP requests** with the `requests` library
2. **OpenAI Python client** pointed to your local server
3. **Curl command examples** for testing from command line

## API Usage

### Using with OpenAI Client

You can use the standard OpenAI Python client by pointing it to your proxy server:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="dummy-key"  # Your GROQ_API_KEY from .env will be used
)

response = client.chat.completions.create(
    model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### Using with HTTP Requests

```bash
curl -X POST "http://localhost:8000/v1/chat/completions" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "groq/llama-3.3-70b-versatile",
       "messages": [
         {"role": "user", "content": "Hello!"}
       ],
       "temperature": 0.7,
       "max_tokens": 100
     }'
```

### Supported Models

The proxy supports these Groq models out of the box:
- `groq/llama-3.3-70b-versatile`
- `groq/llama-3.1-8b-instant`
- `groq/deepseek-r1-distill-llama-70b`
- `groq/meta-llama/llama-4-maverick-17b-128e-instruct`
- `groq/meta-llama/llama-4-scout-17b-16e-instruct`

## Customization

This template is designed to be a foundation for building production AI infrastructure. Key areas for customization:

### Basic Customization
- **Model Selection:** Update supported models in the `/v1/models` endpoint
- **Environment Config:** Add new environment variables for different providers
- **Request Validation:** Extend Pydantic models for additional parameters

### Advanced Patterns

The proxy architecture enables powerful patterns you can implement:

#### Usage Tracking and Budgets
Track spending per user, team, or API key:
```python
# Add user/team identification to requests
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest, user_id: str = Header(None)):
    # Track usage per user
    usage_tracker.log_request(user_id, request.model, len(request.messages))
    
    # Check budget limits
    if usage_tracker.exceeds_budget(user_id):
        raise HTTPException(status_code=429, detail="Budget exceeded")
```

#### Smart Caching for Cost Savings
Cache frequent responses to reduce API calls:
```python
# Simple caching example
cache_key = hashlib.md5(f"{request.model}{request.messages}".encode()).hexdigest()
if cache_key in response_cache:
    return cached_response
```

#### Enhanced Features
- **Advanced Caching:** Add Redis for distributed response caching
- **Rate Limiting:** Implement per-user, per-team, or per-API-key limits
- **Budget Management:** Set spending limits and alerts
- **Usage Analytics:** Track patterns, costs, and performance metrics
- **Content Filtering:** Add safety checks before/after LLM calls

### Enterprise Use Cases

- **Centralized AI Governance:** All teams use one gateway with unified policies and controls
- **Cost Management:** Track spending across departments and implement budget controls
- **Usage Analytics:** Monitor AI adoption patterns and optimize resource allocation
- **Compliance:** Add audit logging, content filtering, and security controls in one place

## Deployment

### Local Development
```bash
uv run server.py
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn server:app --host 0.0.0.0 --port 8000
```

### Docker Deployment
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install uv && uv sync
CMD ["uv", "run", "server.py"]
```

## Configuration

Configure the server using environment variables:

- `GROQ_API_KEY` - Your Groq API key (required)
- `PORT` - Server port (default: 8000)

## Benefits of the Centralized Gateway Pattern

1. **OpenAI Compatibility:** Use any OpenAI-compatible client or tool
2. **Cost Visibility:** Track spending across users, teams, and projects
3. **Budget Control:** Implement spending limits and usage quotas
4. **Performance Optimization:** Cache responses and monitor usage patterns
5. **Centralized Governance:** Manage policies, security, and compliance from one place
6. **Usage Analytics:** Gain insights into AI adoption and optimization opportunities

## Next Steps

### Quick Start with Production Features

For detailed setup of advanced LiteLLM features:
- [Configuration of Spend Tracking for Keys, Users, and Teams](https://docs.litellm.ai/docs/proxy/cost_tracking)
- [Configuration for Budgets and Rate Limits](https://docs.litellm.ai/docs/proxy/users)

For more information on building production-ready applications with LiteLLM and Groq:
- [Official Documentation: LiteLLM](https://docs.litellm.ai/docs/providers/groq)
- [Tutorial: Groq API Cookbook](https://github.com/groq/groq-api-cookbook/tree/main/tutorials/litellm-proxy-groq)

### For Developers
- **Create your free GroqCloud account:** Access official API docs, the playground for experimentation, and more resources via [Groq Console](https://console.groq.com).
- **Explore LiteLLM:** Check out the [LiteLLM documentation](https://docs.litellm.ai/) for advanced features like budget management and caching
- **Build and customize:** Fork this repo and start customizing to build out your own AI infrastructure
- **Get support:** Connect with other developers building on Groq, chat with our team, and submit feature requests on our [Groq Developer Forum](https://community.groq.com).

### For Founders and Business Leaders
- **See enterprise capabilities:** This template showcases production-ready AI infrastructure that can handle business workloads with centralized control and fast response times
- **Discuss your needs:** [Contact our team](https://groq.com/enterprise-access/) to explore how Groq can accelerate your AI initiatives

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Created by the Groq team using [LiteLLM](https://litellm.ai) and [Groq](https://groq.com). 