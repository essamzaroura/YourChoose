# app.py - Main Flask application
import os
import sys
from backend.models.recommendation_engine import RecommendationEngine

# Ensure the backend and models directories are in sys.path
backend_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, backend_path)
sys.path.insert(0, os.path.join(backend_path, 'models'))


# Flask imports
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules AFTER modifying sys.path
try:
    from models.recommendation_engine import RecommendationEngine
    from models.user import User
except ModuleNotFoundError as e:
    print(f"Module Import Error: {e}")
    print("Make sure the 'models' folder contains '__init__.py' and is properly structured.")
    sys.exit(1)

# Initialize Flask app

app = Flask(__name__)

@app.route("/")  # This defines a route for the homepage
def home():
    return "Welcome to YourChoose-Project API!"
CORS(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
jwt = JWTManager(app)

# Initialize recommendation engine
rec_engine = RecommendationEngine()

@app.route('/api/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    user_id = request.json.get('user_id')
    query = request.json.get('query', '')
    context = request.json.get('context', {})

    recommendations = rec_engine.generate_recommendations(user_id, query, context)
    
    return jsonify({'success': True, 'recommendations': recommendations})

@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.authenticate(username, password)
    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user["id"])
    return jsonify({'success': True, 'token': access_token})

if __name__ == '__main__':
    app.run(debug=True)