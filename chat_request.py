import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_coaching_response(user_message: str, user_context: dict) -> str:
    is_meal_plan = user_context.get('request_type') == 'meal_plan'
    
    system_prompt = """You are a supportive and knowledgeable weight loss coach. 
    Provide encouraging, science-based advice for healthy and sustainable weight loss. 
    Keep responses concise and actionable. Include specific recommendations when appropriate."""
    
    if is_meal_plan:
        system_prompt += """ Focus on providing a balanced meal plan that includes:
        - Specific meal suggestions for breakfast, lunch, dinner, and snacks
        - Approximate calorie counts and macronutrient breakdown
        - Easy-to-find ingredients and simple preparation methods
        - Tips for portion control and meal timing"""
    
    context_str = f"User's current weight: {user_context.get('weight', 'unknown')}kg\n"
    context_str += f"Recent progress: {user_context.get('progress', 'unknown')}\n"
    
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context_str}\nUser message: {user_message}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm having trouble processing your request. Please try again later. Error: {str(e)}"
