from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
def estimate_token_count(text):
    # Placeholder implementation
    return len(text.split())

def split_into_parts(text, token_limit=100000):
    words = text.split()
    parts = []
    current_part = []
    current_count = 0
    
    for word in words:
        if current_count + len(word) + 1 <= token_limit:  # +1 for space
            current_part.append(word)
            current_count += len(word) + 1
        else:
            parts.append(" ".join(current_part))
            current_part = [word]
            current_count = len(word) + 1
    if current_part:
        parts.append(" ".join(current_part))
    return parts

def summarize_with_gpt4(text):
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
          {
        "role": "system",
        "content": "Du er en tekst-oppsummerer. Du oppsummerer gjerne tekst som gir gitt deg, både lang og kort tekst.",
          },
           {
        "role": "user",
        "content": """Under følger et opptak (automatisk transkribrert, noe feil og rare tolkninger kan nok forekomme).\n
"""  + text,
        }
       
    ],
    )
    print(response)
    return response.choices[0].message.content.strip()

def summarize_text(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        
        token_limit = 90000
        estimated_tokens = estimate_token_count(text)
        
        summaries = []
        
        if estimated_tokens > token_limit:
            parts = split_into_parts(text, token_limit)
            for part in parts:
                summary = summarize_with_gpt4(part)
                summaries.append(summary)
            final_summary = summarize_with_gpt4(" ".join(summaries))
        else:
            final_summary = summarize_with_gpt4(text)
        
        print("Summary:")
        print(final_summary)
        
    except Exception as e:
        print(f"Error summarizing text: {e}")
