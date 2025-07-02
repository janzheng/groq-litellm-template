uv init
uv venv
uv add litellm dotenv

# Universal LLM Adapter Pattern

## What We Built
The FastAPI server is essentially an OpenAI API "impersonator" that can route requests to any backend through LiteLLM.

## The Pattern:
**Client** → Makes OpenAI-formatted request → **Your FastAPI Proxy** → **LiteLLM** → **Any LLM Provider**

## Key Concept: Universal OpenAI Interface
Any tool that expects OpenAI's API can now use:
- Groq (like we set up)
- Anthropic Claude
- Google Gemini
- Azure OpenAI
- AWS Bedrock
- Local models (Ollama, etc.)
- And 100+ other providers

## Drop-in Replacement
You can literally take any application using OpenAI and just change the `base_url`:

```python
# Instead of this:
client = OpenAI(api_key="sk-...")

# Use this:
client = OpenAI(
    base_url="http://your-proxy:8000/v1",
    api_key="dummy"
)
```

## Advanced Examples

### 1. Multi-Provider Router
```python
@app.post("/v1/chat/completions")
async def smart_router(request: ChatCompletionRequest):
    model = request.model
    
    # Route different models to different providers
    if "gpt" in model:
        # Use OpenAI
        response = litellm.completion(
            model="gpt-4",
            messages=messages,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    elif "claude" in model:
        # Use Anthropic
        response = litellm.completion(
            model="anthropic/claude-3-sonnet-20240229",
            messages=messages,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    elif "llama" in model:
        # Use Groq
        response = litellm.completion(
            model="groq/llama-3.3-70b-versatile",
            messages=messages,
            api_key=os.getenv("GROQ_API_KEY")
        )
    
    return response
```

### 2. Cost Optimizer with Fallback
```python
@app.post("/v1/chat/completions")
async def cost_optimizer(request: ChatCompletionRequest):
    # Define providers by cost (cheapest first)
    providers = [
        {"model": "groq/llama-3.3-70b-versatile", "cost_per_token": 0.00001},
        {"model": "anthropic/claude-3-haiku-20240307", "cost_per_token": 0.00005},
        {"model": "gpt-4o-mini", "cost_per_token": 0.0001},
    ]
    
    for provider in providers:
        try:
            response = litellm.completion(
                model=provider["model"],
                messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            return response
        except Exception as e:
            print(f"Provider {provider['model']} failed: {e}")
            continue
    
    raise HTTPException(status_code=500, detail="All providers failed")
```

### 3. Enhanced Proxy with Features
```python
import time
import hashlib
from functools import lru_cache

# Simple in-memory cache
response_cache = {}

@app.post("/v1/chat/completions")
async def enhanced_proxy(request: ChatCompletionRequest):
    # Generate cache key
    cache_key = hashlib.md5(
        f"{request.model}{request.messages}{request.temperature}".encode()
    ).hexdigest()
    
    # Check cache first
    if cache_key in response_cache:
        cached_response, timestamp = response_cache[cache_key]
        if time.time() - timestamp < 300:  # 5 minute cache
            return cached_response
    
    # Log the request
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Request to {request.model}")
    
    # Rate limiting (simple example)
    # In production, use Redis or proper rate limiting
    
    # Content filtering
    user_message = request.messages[-1].content
    if any(word in user_message.lower() for word in ["harmful", "illegal"]):
        raise HTTPException(status_code=400, detail="Content not allowed")
    
    try:
        # Make the actual call
        response = litellm.completion(
            model=request.model,
            messages=[{"role": msg.role, "content": msg.content} for msg in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Cache the response
        response_cache[cache_key] = (response, time.time())
        
        # Log success
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Success: {len(response.choices[0].message.content)} chars")
        
        return response
        
    except Exception as e:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

## Real-World Use Cases

### Enterprise
- **Centralize all LLM access** through one endpoint
- **Unified billing and monitoring** across all teams
- **Security and compliance** controls in one place

### Development
- **Switch between providers** without code changes
- **A/B test different models** transparently
- **Local development** with different models than production

### Cost Control
- **Route to cheapest provider** automatically
- **Set spending limits** per user/team
- **Track usage** across all models

### Compliance & Safety
- **Content filtering** before sending to LLM
- **Response filtering** before returning to user
- **Audit logging** of all requests/responses
- **PII detection and removal**

## Benefits
1. **OpenAI Compatibility**: Use any OpenAI-compatible client or tool
2. **Provider Flexibility**: Switch providers without changing client code
3. **Cost Optimization**: Route to most cost-effective models
4. **Reliability**: Implement fallbacks and retry logic
5. **Observability**: Add logging, metrics, and monitoring
6. **Security**: Centralized authentication and content filtering

You've essentially created a "universal LLM adapter" that makes any LLM provider look like OpenAI to your applications!