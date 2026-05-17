// frontend/src/App.js
import { useState } from "react";
import axios from "axios";
import "./App.css";

const API = process.env.REACT_APP_API_URL;

function App() {
  const [jobRole, setJobRole] = useState("");
  const [questions, setQuestions] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Weekend 3 state
  const [answers, setAnswers] = useState({});
  const [feedbacks, setFeedbacks] = useState({});
  const [evaluating, setEvaluating] = useState({});

  const generateQuestions = async () => {
    if (!jobRole.trim()) return;
    setLoading(true);
    setError("");
    setQuestions([]);
    setAnswers({});
    setFeedbacks({});

    try {
      const res = await axios.post(`${API}/generate-questions`, {
        job_role: jobRole,
      });
      setQuestions(res.data.questions);
      setSessionId(res.data.session_id);
    } catch (err) {
      setError("Failed to generate questions. Check if backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const evaluateAnswer = async (questionIndex, question) => {
    const answer = answers[questionIndex];
    if (!answer?.trim()) return;

    setEvaluating((prev) => ({ ...prev, [questionIndex]: true }));

    try {
      const res = await axios.post(`${API}/evaluate-answer`, {
        session_id: sessionId,
        question: question,
        answer: answer,
      });
      setFeedbacks((prev) => ({ ...prev, [questionIndex]: res.data }));
    } catch (err) {
      alert("Failed to evaluate answer");
    } finally {
      setEvaluating((prev) => ({ ...prev, [questionIndex]: false }));
    }
  };

  return (
    <div className="container">
      <h1>🎯 AI Interview Coach</h1>
      <p className="subtitle">Generate role-specific questions and get AI feedback on your answers</p>

      <div className="input-section">
        <input
          type="text"
          placeholder="Enter job role (e.g. Java Backend Engineer, React Developer)"
          value={jobRole}
          onChange={(e) => setJobRole(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && generateQuestions()}
        />
        <button onClick={generateQuestions} disabled={loading || !jobRole.trim()}>
          {loading ? "Generating..." : "Generate Questions"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {questions.length > 0 && (
        <div className="questions-section">
          <h2>Interview Questions for: <span>{jobRole}</span></h2>
          {questions.map((question, i) => (
            <div key={i} className="question-card">
              <p className="question-text">
                <strong>Q{i + 1}.</strong> {question}
              </p>

              {/* Answer input - Weekend 3 feature */}
              <textarea
                placeholder="Type your answer here..."
                value={answers[i] || ""}
                onChange={(e) =>
                  setAnswers((prev) => ({ ...prev, [i]: e.target.value }))
                }
                rows={4}
              />
              <button
                className="evaluate-btn"
                onClick={() => evaluateAnswer(i, question)}
                disabled={evaluating[i] || !answers[i]?.trim()}
              >
                {evaluating[i] ? "Evaluating..." : "Get AI Feedback"}
              </button>

              {feedbacks[i] && (
                <div className="feedback-card">
                  <div className="score">
                    Score: <span>{feedbacks[i].score}/10</span>
                  </div>
                  <p>{feedbacks[i].feedback}</p>
                  <h4>How to improve:</h4>
                  <ul>
                    {feedbacks[i].improvements.map((imp, j) => (
                      <li key={j}>{imp}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
