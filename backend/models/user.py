# models/user.py
class User:
    # Simulated user data (replace with a real database)
    USERS = {
        "testuser": {"password": "password123", "id": 1},
        "admin": {"password": "admin123", "id": 2}
    }

    @staticmethod
    def authenticate(username, password):
        user = User.USERS.get(username)
        if user and user["password"] == password:
            return user  # Return user object (or ID)
        return None  # Authentication failed
