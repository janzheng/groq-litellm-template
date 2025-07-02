import os
import litellm
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="LiteLLM Proxy Server",
    description="OpenAI-compatible API proxy using LiteLLM with Groq backend",
    version="1.0.0"
)

# Pydantic models for request/response
class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "groq/llama-3.3-70b-versatile"
    messages: List[Message]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = None
    top_p: Optional[float] = 1.0
    frequency_penalty: Optional[float] = 0.0
    presence_penalty: Optional[float] = 0.0
    stop: Optional[List[str]] = None
    stream: Optional[bool] = False

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]

@app.get("/")
async def root():
    return {"message": "LiteLLM Proxy Server is running"}

@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI-compatible endpoint)"""
    return {
        "object": "list",
        "data": [
            {
                "id": "groq/llama-3.3-70b-versatile",
                "object": "model",
                "created": 1234567890,
                "owned_by": "groq"
            },
            {
                "id": "groq/llama-3.1-8b-instant", 
                "object": "model",
                "created": 1234567890,
                "owned_by": "groq"
            },
            {
                "id": "groq/deepseek-r1-distill-llama-70b",
                "object": "model", 
                "created": 1234567890,
                "owned_by": "groq"
            },
            {
                "id": "groq/meta-llama/llama-4-maverick-17b-128e-instruct",
                "object": "model", 
                "created": 1234567890,
                "owned_by": "groq"
            },
            {
                "id": "groq/meta-llama/llama-4-scout-17b-16e-instruct",
                "object": "model", 
                "created": 1234567890,
                "owned_by": "groq"
            },
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """OpenAI-compatible chat completions endpoint"""
    try:
        # Convert Pydantic messages to dict format for litellm
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Prepare litellm parameters
        litellm_params = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
            "top_p": request.top_p,
            "frequency_penalty": request.frequency_penalty,
            "presence_penalty": request.presence_penalty,
            "stop": request.stop,
            "stream": request.stream
        }
        
        # Remove None values
        litellm_params = {k: v for k, v in litellm_params.items() if v is not None}
        
        # Make the call to litellm
        response = litellm.completion(**litellm_params)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/chat/completions")
async def chat_completions_simple(request: ChatCompletionRequest):
    """Simplified endpoint without /v1 prefix"""
    return await chat_completions(request)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 