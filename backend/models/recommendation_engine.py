import google.generativeai as genai
from backend.database import get_user_preferences, update_user_preferences
from backend.config import GEMINI_API_KEY

class RecommendationEngine:
    def __init__(self):
        # Initialize Gemini AI with the imported key
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")

    def generate_recommendations(self, user_id, query='', context={}):
        user_prefs = get_user_preferences(user_id)
        prompt = self._construct_prompt(query, user_prefs, context)

        try:
            response = self.model.generate_content(prompt)
            recommendations = self._parse_response(response.text)
            self._update_user_preferences(user_id, query, recommendations)
            return recommendations
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            return []  # Return an empty list or handle the error appropriately

    def _construct_prompt(self, query, user_prefs, context):
        # Construct the prompt based on your needs
        prompt = f"User Query: {query}\nUser Preferences: {user_prefs}\nContext: {context}\nProvide recommendations."
        return prompt

    def _parse_response(self, response_text):
        # Parse the response text to extract recommendations
        # This part depends on the format of the Gemini response
        # You'll need to customize this based on Gemini's output
        # Example: if the response is a list separated by newlines
        recommendations = [item.strip() for item in response_text.split('\n') if item.strip()]
        return recommendations

    def _update_user_preferences(self, user_id, query, recommendations):
        # Update user preferences based on interactions
        # This part depends on your database schema and logic
        # Example: you might track queries and recommendations
        update_user_preferences(user_id, query, recommendations)