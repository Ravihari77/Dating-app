# chatbot.py (Updated to only call APIs)
import requests
import json

API_BASE_URL = "http://127.0.0.1:5000"

def get_personality_questions_from_api():
    api_url = f"{API_BASE_URL}/get_personality_questions"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting personality questions: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding questions API response.")
        return None

def submit_answers_to_api(answers):
    api_url = f"{API_BASE_URL}/submit_answers"
    payload = json.dumps({"answers": answers})
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(api_url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('personality_type')
    except requests.exceptions.RequestException as e:
        print(f"Error submitting answers: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding submit answers API response.")
        return None

def get_matches_from_api(personality_type):
    api_url = f"{API_BASE_URL}/get_matches"
    payload = json.dumps({"personality_type": personality_type})
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(api_url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()
        return data.get('matches')
    except requests.exceptions.RequestException as e:
        print(f"Error getting matches: {e}")
        return None
    except json.JSONDecodeError:
        print("Error decoding matches API response.")
        return None

if __name__ == "__main__":
    print("Welcome to the Personality Chatbot!")
    input("Press Enter to start the personality assessment...")

    questions = get_personality_questions_from_api()
    if questions:
        user_answers = []
        print("\nAnswer the following questions:")
        for i, q_data in enumerate(questions):
            question = q_data['question']
            options = q_data['options']
            print(f"\n{i+1}. {question}\nA) {options['A']}\nB) {options['B']}\n(Answer A or B)")
            while True:
                user_answer = input("You: ").strip().upper()
                if user_answer in ["A", "B"]:
                    user_answers.append(user_answer)
                    break
                else:
                    print("Invalid input. Please enter A or B.")

        if len(user_answers) == 12:
            personality = submit_answers_to_api(user_answers)
            if personality:
                print(f"\nYour determined personality type is: {personality}")
                ask_for_matches = input("Would you like to find your best matches? (yes/no): ").lower()
                if ask_for_matches == "yes":
                    matches = get_matches_from_api(personality)
                    if matches:
                        print("\nYour potential matches:")
                        for match in matches:
                            print(f"- {match['name']} ({match['personality']}): Compatibility Score - {match['score']:.2f}")
                    else:
                        print("Could not retrieve personality matches.")
                else:
                    print("Okay, maybe later!")
            else:
                print("Could not determine your personality type.")
        else:
            print("Could not collect all the answers.")
    else:
        print("Failed to retrieve personality questions.")

    print("\nThank you for using the Personality Chatbot!")