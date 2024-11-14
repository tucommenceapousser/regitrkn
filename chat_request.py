import os
from openai import OpenAI

def get_api_key():
    # Try multiple API keys in order
    for key_name in ["OPENAI_API_KEY", "OPENAI_API_KEY1", "OPENAI_API_KEY2"]:
        key = os.environ.get(key_name)
        if key:
            return key
    return None

def get_openai_client():
    api_key = get_api_key()
    if not api_key:
        raise ValueError("No valid OpenAI API key found")
    return OpenAI(api_key=api_key)

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
            system_prompt += """ En tant que coach nutritionnel, créez un plan de repas détaillé qui:
            - Fournit des suggestions spécifiques pour chaque repas de la journée
            - Inclut des collations saines
            - Précise les calories et macronutriments approximatifs
            - Utilise des ingrédients courants et des méthodes de préparation simples
            - Donne des conseils pour la préparation et le contrôle des portions
            
            Format de réponse:
            Petit-déjeuner (XXX calories):
            - Repas suggéré
            - Ingrédients et préparation
            - Macronutriments
            
            Collation Matin (XXX calories):
            [même format]
            
            Déjeuner (XXX calories):
            [même format]
            
            Collation Après-midi (XXX calories):
            [même format]
            
            Dîner (XXX calories):
            [même format]
            
            Conseils supplémentaires:
            - Conseil 1
            - Conseil 2"""
        else:
            system_prompt += """ As a nutrition coach, create a detailed meal plan that:
            - Provides specific suggestions for each meal of the day
            - Includes healthy snacks
            - Specifies approximate calories and macronutrients
            - Uses common ingredients and simple preparation methods
            - Gives tips for preparation and portion control
            
            Response format:
            Breakfast (XXX calories):
            - Suggested meal
            - Ingredients and preparation
            - Macronutrients
            
            Morning Snack (XXX calories):
            [same format]
            
            Lunch (XXX calories):
            [same format]
            
            Afternoon Snack (XXX calories):
            [same format]
            
            Dinner (XXX calories):
            [same format]
            
            Additional Tips:
            - Tip 1
            - Tip 2"""
    
    weight = user_context.get('weight', 'unknown')
    height = user_context.get('height', 'unknown')
    activity_level = user_context.get('activity_level', 'moderate')
    
    context_str = f"Poids actuel: {weight}kg\n" if is_french else f"Current weight: {weight}kg\n"
    if height != 'unknown':
        context_str += f"Taille: {height}cm\n" if is_french else f"Height: {height}cm\n"
    context_str += f"Niveau d'activité: {activity_level}\n" if is_french else f"Activity level: {activity_level}\n"
    
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context_str}\nUser message: {user_message}"}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return str(response.choices[0].message.content)
    except ValueError as ve:
        return "Erreur de configuration: Clé API manquante" if is_french else "Configuration error: Missing API key"
    except Exception as e:
        return "Une erreur s'est produite. Veuillez réessayer plus tard." if is_french else "An error occurred. Please try again later."
