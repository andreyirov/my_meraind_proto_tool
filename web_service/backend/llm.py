import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the root directory
load_dotenv() 
if not os.getenv("API_KEY"):
    load_dotenv(dotenv_path="../../.env")

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL", "deepseek-chat")

if not API_KEY:
    print("Warning: API_KEY not found in environment variables.")

try:
    client = OpenAI(
        api_key=API_KEY,
        base_url=BASE_URL,
    )
except Exception as e:
    client = None
    print(f"Error initializing OpenAI client: {e}")

def generate_diagram_code(diagram_type: str, description: str, current_diagram: str = None) -> str:
    if not client:
        return "Error: OpenAI client not initialized."

    # Specific instructions based on diagram type
    type_instruction = ""
    if diagram_type == "sequence":
        type_instruction = "Start with 'sequenceDiagram'. Use '->>' for solid lines and '-->>' for dotted lines."
    elif diagram_type == "flowchart":
        type_instruction = "Start with 'graph TD' (or LR/TB). Use valid Mermaid flowchart syntax."

    system_prompt = f"""
    You are an expert in Mermaid.js diagram generation.
    Your task is to generate or update a {diagram_type} diagram based on the user's description.
    
    {type_instruction}
    
    CRITICAL INSTRUCTIONS:
    1. Output ONLY the valid Mermaid code. 
    2. Do NOT include markdown formatting (like ```mermaid or ```).
    3. Do NOT include explanations, preambles, or postscripts. Just the code.
    4. Ensure all syntax is valid for Mermaid.js.
    
    If the user provides feedback on an existing diagram, modify the existing code accordingly while preserving the rest of the logic.
    """
    
    user_content = f"Request: {description}"
    if current_diagram:
        user_content += f"\n\nCurrent Diagram Code:\n{current_diagram}"
        
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
        )
        content = response.choices[0].message.content.strip()
        
        # Aggressive cleanup of markdown code blocks
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.strip().startswith('```'):
                continue
            cleaned_lines.append(line)
        
        content = '\n'.join(cleaned_lines).strip()
        
        return content
    except Exception as e:
        return f"Error generating diagram: {str(e)}"
