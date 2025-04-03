# app.py - Main Flask Application with Gemini AI for Chat and Recommendations

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai  # Import Gemini AI SDK

# Ensure the backend and models directories are in sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# Import modules AFTER modifying sys.path
try:
    from models.recommendation_engine import RecommendationEngine
    from config import GEMINI_API_KEY  # Load API Key securely
except ModuleNotFoundError as e:
    print(f"Module Import Error: {e}")
    print("Make sure the 'models' folder contains '__init__.py' and is properly structured.")
    sys.exit(1)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set Gemini API Key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize recommendation engine
rec_engine = RecommendationEngine()

@app.route("/")
def home():
    """Home route displaying welcome message."""
    return "Welcome to YourChoose-Project API! Home Page with Recommendations & AI Chat."

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """Generates AI-powered recommendations based on user input."""
    user_id = request.json.get('user_id')
    query = request.json.get('query', '')
    context = request.json.get('context', {})

    recommendations = rec_engine.generate_recommendations(user_id, query, context)
    
    return jsonify({'success': True, 'recommendations': recommendations})

@app.route("/api/chat", methods=["POST"])
def chat():
    """Handles AI chatbot interactions using Gemini AI, summarizing in plain language."""
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"You are a professional journalist summarizing: {user_input}")
        reply = response.text
    except Exception as e:
        return jsonify({"error": f"Failed to process AI response: {str(e)}"}), 500

    return jsonify({"response": reply})


if __name__ == '__main__':
    app.run(debug=True)