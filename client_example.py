import requests
import json

# Example 1: Using requests library
def test_with_requests():
    url = "http://localhost:8000/v1/chat/completions"
    
    payload = {
        "model": "groq/llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": "Hello! Can you tell me a joke?"}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        print("Response from server:")
        print(json.dumps(result, indent=2))
        
        # Extract just the message content
        if 'choices' in result and len(result['choices']) > 0:
            message = result['choices'][0]['message']['content']
            print(f"\nAssistant: {message}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")

# Example 2: Using OpenAI client (pointing to local server)
def test_with_openai_client():
    try:
        from openai import OpenAI
        
        # Point OpenAI client to your local server
        client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="dummy-key"  # LiteLLM will use your GROQ_API_KEY from env
        )
        
        response = client.chat.completions.create(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "What's the capital of France?"}
            ],
            temperature=0.5,
            max_tokens=100
        )
        
        print("OpenAI client response:")
        print(f"Assistant: {response.choices[0].message.content}")
        
    except ImportError:
        print("OpenAI library not installed. Install with: pip install openai")
    except Exception as e:
        print(f"Error with OpenAI client: {e}")

# Example 3: Curl command equivalent
def show_curl_example():
    curl_command = '''
curl -X POST "http://localhost:8000/v1/chat/completions" \\
     -H "Content-Type: application/json" \\
     -d '{
       "model": "groq/llama-3.3-70b-versatile",
       "messages": [
         {"role": "user", "content": "Hello from curl!"}
       ],
       "temperature": 0.7,
       "max_tokens": 100
     }'
    '''
    print("Equivalent curl command:")
    print(curl_command)

if __name__ == "__main__":
    print("Testing LiteLLM Proxy Server...")
    print("Make sure the server is running with: python server.py")
    print("=" * 50)
    
    # Test server availability
    try:
        response = requests.get("http://localhost:8000/")
        print(f"Server status: {response.json()}")
        print("=" * 50)
    except:
        print("Server not running! Start it with: python server.py")
        exit(1)
    
    # Run tests
    print("\n1. Testing with requests library:")
    test_with_requests()
    
    print("\n" + "=" * 50)
    print("\n2. Testing with OpenAI client:")
    test_with_openai_client()
    
    print("\n" + "=" * 50)
    print("\n3. Curl example:")
    show_curl_example() 