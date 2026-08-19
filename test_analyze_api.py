import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import json

slides_data = [
    {
        "id": 1,
        "number": 1,
        "title": "Grocery List",
        "bullets": ["Milk", "Eggs", "Bread"]
    }
]

slides_text = ''
for s in slides_data:
    slides_text += f'\nSlide {s.get("number", "?")}: {s.get("title", "")}\n'
    for b in s.get('bullets', []):
        slides_text += f'  - {b}\n'

system_prompt = """You are an expert instructional designer specializing in Bloom's Taxonomy.
Your task is to analyze presentation slides and return a JSON response with the exact structure requested.
Be concise, practical, and actionable in your suggestions."""

user_prompt = f"""Analyze these presentation slides and for each slide provide:
1. Bloom's Taxonomy classification (one of: remember, understand, apply, analyze, evaluate, create)
2. AI classification reasoning (1-2 sentences)
3. 2-3 specific, actionable improvement suggestions to better align with that level
4. A short, engaging explanation of the slide directly addressing the student, explicitly utilizing the assigned taxonomy level's framing (e.g., if 'Apply', explain how they would apply this; if 'Analyze', explain how to break it down).
5. 2-3 student questions at that taxonomy level to help students understand the content

Bloom's levels reference:
- remember: Recall, List, Name, Define, Recognize
- understand: Explain, Summarize, Classify, Paraphrase
- apply: Demonstrate, Solve, Execute, Implement
- analyze: Differentiate, Compare, Examine, Deconstruct
- evaluate: Judge, Critique, Justify, Defend
- create: Design, Build, Construct, Compose

SLIDES:
{slides_text}

Respond ONLY with valid JSON in this exact structure:
{{
  "slides": [
    {{
      "id": 1,
      "taxonomyLevel": "remember",
      "aiNotes": "Brief reason why this taxonomy level was assigned.",
      "suggestions": [
        "Actionable improvement suggestion 1",
        "Actionable improvement suggestion 2"
      ],
      "studentExplanation": "Engaging explanation of the slide for the student using the taxonomy framing.",
      "studentQuestions": [
        {{"question": "Question that helps students understand?", "answer": "Concise answer/hint for the student."}},
        {{"question": "Another learning question?", "answer": "Answer hint."}}
      ]
    }}
  ]
}}"""

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user',   'content': user_prompt}
        ],
        response_format={'type': 'json_object'},
        temperature=0.3,
        max_tokens=16000
    )
    print("Success:")
    print(response.choices[0].message.content)
except Exception as e:
    import traceback; traceback.print_exc()
