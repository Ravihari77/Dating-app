# app.py (Updated to serve questions)
from flask import Flask, request, jsonify
import json
import random
from match import find_best_matches

app = Flask(__name__)

personality_questions = {
    "EI": [
        ("How do you prefer to spend your weekends?", "A) Going out with friends and socializing.", "B) Relaxing alone or with a small group.", "E", "I"),
        ("Which best describes you at a party?", "A) I enjoy talking to many people and meeting new ones.", "B) I prefer deeper conversations with a few close friends.", "E", "I"),
        ("You get a surprise invitation to an event where you don’t know anyone. What do you do?", "A) I feel excited about the chance to meet new people.", "B) I feel nervous and prefer staying in my comfort zone.", "E", "I"),
    ],
    "SN": [
        ("When learning something new, do you prefer:", "A) Practical, hands-on examples and real-life applications.", "B) Exploring theories, patterns, and abstract concepts.", "S", "N"),
        ("What kind of activities excite you more?", "A) Physical, hands-on experiences (e.g., sports, DIY projects).", "B) Mental and creative challenges (e.g., puzzles, brainstorming).", "S", "N"),
        ("You are given a difficult puzzle to solve. How do you approach it?", "A) I carefully analyze each piece and focus on details.", "B) I step back, look at the bigger picture, and try different ideas.", "S", "N"),
    ],
    "TF": [
        ("How do you usually make decisions?", "A) Based on logic, facts, and analysis.", "B) Based on feelings and how it affects others.", "T", "F"),
        ("How do you handle stress?", "A) I focus on solving the problem logically.", "B) I rely on emotional support and intuition.", "T", "F"),
        ("Your friend is going through a tough time and asks for your help. What do you do?", "A) Give them logical advice on how to solve their problem.", "B) Listen, empathize, and offer emotional support.", "T", "F"),
    ],
    "JP": [
        ("Which best describes your work style?", "A) I like making a schedule and following it.", "B) I prefer going with the flow and adapting as I go.", "J", "P"),
        ("When planning a trip, do you:", "A) Research and plan everything in detail.", "B) Keep things flexible and decide along the way.", "J", "P"),
        ("You are leading a team on an important project. What approach do you take?", "A) I assign clear roles, set deadlines, and follow a structured plan.", "B) I let the team explore different ideas freely before deciding.", "J", "P"),
    ],
}

@app.route('/get_personality_questions', methods=['GET'])
def get_personality_questions_api():
    # Prepare a list of questions, each with the question text and options
    questions_list = []
    for category in personality_questions.values():
        for question, option_a, option_b, _, _ in category:
            questions_list.append({"question": question, "options": {"A": option_a, "B": option_b}})
    random.shuffle(questions_list)  # Shuffle the order of questions
    return jsonify(questions_list), 200

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    try:
        data = request.get_json()
        answers = data.get('answers')

        if not answers or not isinstance(answers, list) or len(answers) != 12:
            return jsonify({'error': 'Please provide a list of 12 answers (A or B)'}), 400

        personality_score = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
        categories = ["EI", "SN", "TF", "JP"]
        question_index = 0
        question_map = {
            "EI": ["E", "I"],
            "SN": ["S", "N"],
            "TF": ["T", "F"],
            "JP": ["J", "P"],
        }

        # Reconstruct the original question order to correctly map answers
        all_questions = []
        for category in personality_questions.values():
            for q, a, b, t1, t2 in category:
                all_questions.append(((q, a, b), t1, t2))

        # Assuming the chatbot received the questions in the order served by /get_personality_questions
        # We might need a way to track the original traits associated with each question if the order is randomized.
        # A simpler approach is to rely on the fixed structure of personality_questions.

        question_index = 0
        for category_code, traits in question_map.items():
            for i in range(3):
                _, _, _, type_a, type_b = personality_questions[category_code][i]
                user_answer = answers[question_index].strip().upper()
                if user_answer == "A":
                    personality_score[type_a] += 1
                elif user_answer == "B":
                    personality_score[type_b] += 1
                else:
                    return jsonify({'error': f'Invalid answer: "{user_answer}". Please use A or B.'}), 400
                question_index += 1


        mbti_type = "".join([max(pair, key=lambda p: personality_score[p]) for pair in ["EI", "SN", "TF", "JP"]])
        return jsonify({'personality_type': mbti_type}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_matches', methods=['POST'])
def get_matches_api():
    try:
        data = request.get_json()
        personality_type = data.get('personality_type')
        if not personality_type:
            return jsonify({'error': 'Please provide a personality_type'}), 400
        matches = find_best_matches(personality_type)
        return jsonify({'matches': matches}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)