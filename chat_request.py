import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def get_coaching_response(user_message: str, user_context: dict) -> str:
    is_meal_plan = user_context.get('request_type') == 'meal_plan'
    is_french = user_context.get('language') == 'fr'
    
    system_prompt = """You are a supportive and knowledgeable weight loss coach. 
    Provide encouraging, science-based advice for healthy and sustainable weight loss. 
    Keep responses concise and actionable. Include specific recommendations when appropriate."""
    
    if is_french:
        system_prompt = """Vous êtes un coach de perte de poids encourageant et compétent.
        Fournissez des conseils encourageants et scientifiques pour une perte de poids saine et durable.
        Gardez les réponses concises et pratiques. Incluez des recommandations spécifiques lorsque c'est approprié."""
    
    if is_meal_plan:
        if is_french:
            system_prompt += """ Concentrez-vous sur la fourniture d'un plan de repas équilibré qui comprend :
            - Suggestions spécifiques pour le petit-déjeuner, le déjeuner, le dîner et les collations
            - Calories approximatives et répartition des macronutriments
            - Ingrédients faciles à trouver et méthodes de préparation simples
            - Conseils pour le contrôle des portions et le timing des repas"""
        else:
            system_prompt += """ Focus on providing a balanced meal plan that includes:
            - Specific meal suggestions for breakfast, lunch, dinner, and snacks
            - Approximate calorie counts and macronutrient breakdown
            - Easy-to-find ingredients and simple preparation methods
            - Tips for portion control and meal timing"""
    
    context_str = f"Poids actuel de l'utilisateur: {user_context.get('weight', 'unknown')}kg\n" if is_french else f"User's current weight: {user_context.get('weight', 'unknown')}kg\n"
    context_str += f"Progrès récents: {user_context.get('progress', 'unknown')}\n" if is_french else f"Recent progress: {user_context.get('progress', 'unknown')}\n"
    
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
        return "Une erreur s'est produite. Veuillez réessayer plus tard." if is_french else "An error occurred. Please try again later."
