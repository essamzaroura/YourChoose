# models/recommendation_engine.py
import os
import openai
from database import get_user_preferences, update_user_preferences

class RecommendationEngine:
    def __init__(self):
        # Initialize OpenAI API
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = "gpt-4"  # Using GPT-4 for high-quality recommendations
        
    def generate_recommendations(self, user_id, query='', context={}):
        # Get user preferences from database
        user_prefs = get_user_preferences(user_id)
        
        # Prepare prompt for LLM
        prompt = self._construct_prompt(query, user_prefs, context)
        
        # Generate recommendations using LLM
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful recommendation assistant that provides personalized suggestions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,  # As specified in requirements
            temperature=0.2,  # Low temperature for accuracy
            top_p=0.9        # Focus on high-confidence responses
        )
        
        recommendations = self._parse_response(response.choices[0].message['content'])
        
        # Update user preferences based on interaction
        self._update_user_preferences(user_id, query, recommendations)
        
        return recommendations
    
    def _construct_prompt(self, query, user_prefs, context):
        # Combine user query, preferences, and context into a prompt
        prompt = f"Based on the user's query: '{query}'\n"
        prompt += f"And their preferences: {user_prefs}\n"
        prompt += f"And the current context: {context}\n"
        prompt += "Provide 3-5 personalized recommendations."
        return prompt
    
    def _parse_response(self, response_text):
        # Parse the LLM response into structured recommendations
        # This is a simplified example; you might want more complex parsing
        lines = response_text.strip().split('\n')
        recommendations = []
        
        for line in lines:
            if line.strip():
                recommendations.append({
                    'text': line.strip(),
                    'confidence': 0.9  # Placeholder confidence score
                })
        
        return recommendations
    
    def _update_user_preferences(self, user_id, query, recommendations):
        # Update user preferences based on current interaction
        # This would typically involve some machine learning to refine preferences
        update_user_preferences(user_id, query, recommendations)