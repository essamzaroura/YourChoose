import openai
from backend.database import get_user_preferences, update_user_preferences  # ✅ CORRECT
from backend.config import OPENAI_API_KEY


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import OPENAI_API_KEY

class RecommendationEngine:
    def __init__(self):
        # Initialize OpenAI API with the imported key
        openai.api_key = OPENAI_API_KEY
        self.model = "gpt-4"

    def generate_recommendations(self, user_id, query='', context={}):
        user_prefs = get_user_preferences(user_id)
        prompt = self._construct_prompt(query, user_prefs, context)

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful recommendation assistant that provides personalized suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.2,
            top_p=0.9
        )

        recommendations = self._parse_response(response.choices[0].message['content'])
        self._update_user_preferences(user_id, query, recommendations)

        return recommendations
