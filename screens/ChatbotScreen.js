import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList } from 'react-native';

const API_BASE_URL = 'http://192.168.8.120:5000'; // Replace with your machine's IP if running on a physical device

const ChatbotScreen= () => {
  const [messages, setMessages] = useState([]);
  const [currentInput, setCurrentInput] = useState('');
  const [questions, setQuestions] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState([]);
  const [personality, setPersonality] = useState(null);
  const [matches, setMatches] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE_URL}/get_personality_questions`)
      .then(response => response.json())
      .then(data => setQuestions(data))
      .catch(error => console.error('Error fetching questions:', error));
  }, []);

  const handleAnswer = (answer) => {
    setAnswers([...answers, answer]);
    setCurrentQuestionIndex(currentQuestionIndex + 1);
  };

  const handleSubmitAnswers = () => {
    fetch(`${API_BASE_URL}/submit_answers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ answers }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.personality_type) {
          setPersonality(data.personality_type);
          setMessages([...messages, { text: `Your personality type is: ${data.personality_type}`, isUser: false }]);
        } else {
          setMessages([...messages, { text: 'Could not determine personality.', isUser: false }]);
        }
      })
      .catch(error => console.error('Error submitting answers:', error));
  };

  const handleGetMatches = () => {
    if (personality) {
      fetch(`${API_BASE_URL}/get_matches`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ personality_type: personality }),
      })
        .then(response => response.json())
        .then(data => setMatches(data.matches))
        .catch(error => console.error('Error getting matches:', error));
    }
  };

  // ... (Render your UI using messages, questions, currentQuestionIndex, personality, matches, etc.)

  return (
    <View>
      {questions.length > 0 && currentQuestionIndex < questions.length && (
        <View>
          <Text>{questions[currentQuestionIndex].question}</Text>
          <Button title={`A) ${questions[currentQuestionIndex].options.A}`} onPress={() => handleAnswer('A')} />
          <Button title={`B) ${questions[currentQuestionIndex].options.B}`} onPress={() => handleAnswer('B')} />
        </View>
      )}

      {currentQuestionIndex === questions.length && !personality && (
        <Button title="Submit Answers" onPress={handleSubmitAnswers} />
      )}

      {personality && !matches && (
        <Button title="Find Matches" onPress={handleGetMatches} />
      )}

      {matches && (
        <View>
          <Text>Your Potential Matches:</Text>
          <FlatList
            data={matches}
            keyExtractor={(item, index) => index.toString()}
            renderItem={({ item }) => (
              <Text>- {item.name} ({item.personality}): Compatibility Score - {item.score.toFixed(2)}</Text>
            )}
          />
        </View>
      )}

      {/* ... (UI to display messages) ... */}
    </View>
  );
};

export default ChatbotScreen;