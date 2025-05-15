import json
import requests  # For making API requests

# Load sample user database safely
def load_users(file_path="user.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading users: {e}")
        return []

# Compatibility scores based on MBTI pairings
compatibility_matrix = {
    "INFJ": {"ENFJ", "INFP", "INTJ", "INFJ"},
    "ENFJ": {"INFJ", "ENTP", "ESFJ", "ENFJ"},
    "INFP": {"ENFP", "INFJ", "INTP", "ISFP"},
    "INTJ": {"INFJ", "ENTP", "INTP", "INTJ"},
    "ESFJ": {"ISFJ", "ENFJ", "ESTJ", "ESFP"},
    "ISFJ": {"ESFJ", "ISTJ", "ISFP", "INFJ"},
    "ENTP": {"INTP", "ENTJ", "ENFP", "INFJ"},
    "INTP": {"ENTP", "INTJ", "INFP", "ISTP"},
    "ENTJ": {"INTJ", "ENTP", "ENFP", "ESTJ"},
    "ESTJ": {"ISTJ", "ESTP", "ENTJ", "ESFJ"},
    "ENFP": {"INFP", "ENTP", "ENFJ", "ENTJ"},
    "ISTP": {"ESTP", "ISTJ", "INTP", "ISFP"},
    "ESTP": {"ISTP", "ESTJ", "ESFP", "ENTP"},
    "ISTJ": {"ESTJ", "ISFJ", "ISTP", "INTJ"},
    "ISFP": {"ESFP", "ISFJ", "INFP", "ISTP"},
    "ESFP": {"ISFP", "ESFJ", "ESTP", "ENFP"}
}

def find_best_matches(users, mbti_type):
    """Finds the best MBTI matches based on compatibility."""
    return sorted(
        [
            {
                "name": user["name"],
                "personality": user["personality"],
                "score": 1.0 if user["personality"] == mbti_type else 0.85 if user["personality"] in compatibility_matrix.get(mbti_type, set()) else 0.65
            }
            for user in users
        ],
        key=lambda x: x["score"],
        reverse=True
    )

def send_to_api(mbti_type, matches, api_url="http://10.0.2.2:5000/backend/match"):
    """Sends the MBTI type and matches to the API."""
    try:
        response = requests.post(api_url, json={"mbti_type": mbti_type, "matches": matches})
        response.raise_for_status()
        print("API Response:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to API: {e}")

def fetch_user_data(api_url="http://10.0.2.2:5000/backend/user"):
    """Fetches user data from the API."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user data: {e}")
        return []

if __name__ == "__main__":
    from chatbot import get_user_mbti_type  # Import from chatbot.py
    
    mbti_type = get_user_mbti_type()  # Dynamically get MBTI type
    
    users = fetch_user_data() or load_users()  # Use API data if available, fallback to JSON
    
    matches = find_best_matches(users, mbti_type)
    
    send_to_api(mbti_type, matches)

    # Log the match count
    log_data = {"mbti_type": mbti_type, "matches_count": len(matches)}
    send_to_api(log_data, api_url="http://10.0.2.2:5000/api/log")  # Log data