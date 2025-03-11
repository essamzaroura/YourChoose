# app.py - Main Flask application
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os
from dotenv import load_dotenv
from models.recommendation_engine import RecommendationEngine
from models.user import User

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure JWT
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Initialize recommendation engine
rec_engine = RecommendationEngine()

@app.route('/api/recommendations', methods=['POST'])
@jwt_required()
def get_recommendations():
    user_id = request.json.get('user_id')
    query = request.json.get('query', '')
    context = request.json.get('context', {})
    
    # Get personalized recommendations
    recommendations = rec_engine.generate_recommendations(
        user_id=user_id,
        query=query,
        context=context
    )
    
    return jsonify({
        'success': True,
        'recommendations': recommendations
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Authenticate user (simplified for example)
    user = User.authenticate(username, password)
    if not user:
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    return jsonify({'success': True, 'token': access_token})

if __name__ == '__main__':
    app.run(debug=True)