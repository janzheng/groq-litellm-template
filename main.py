import os
import litellm
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get('GROQ_API_KEY')


response = litellm.completion(
    model="groq/llama-3.3-70b-versatile", 
    messages=[
       {"role": "user", "content": "hello from litellm"}
   ],
)
print(response)
