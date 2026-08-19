import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

try:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Hello! Give me JSON: {"slides": []}'}
        ],
        response_format={'type': 'json_object'},
        temperature=0.3,
        max_tokens=16000
    )
    print(response.choices[0].message.content)
except Exception as e:
    import traceback; traceback.print_exc()
