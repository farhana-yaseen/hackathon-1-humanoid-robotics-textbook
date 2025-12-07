import React, { useState, useEffect } from "react";

const BACKEND_URL = "http://127.0.0.1:8000/api/selected-chat-stream";

const Chatbot: React.FC = () => {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [selectedText, setSelectedText] = useState("");

  // Automatically capture selected text from the page
  useEffect(() => {
    const handleSelectionChange = () => {
      const text = window.getSelection()?.toString().trim() || "";
      if (text) setSelectedText(text);
    };

    document.addEventListener("mouseup", handleSelectionChange);
    document.addEventListener("keyup", handleSelectionChange);

    return () => {
      document.removeEventListener("mouseup", handleSelectionChange);
      document.removeEventListener("keyup", handleSelectionChange);
    };
  }, []);

  const handleAsk = async () => {
    if (!question || !selectedText) {
      alert("Please type a question and select some text from the page.");
      return;
    }

    setAnswer("Generating answer...");

    try {
      const response = await fetch(
        `${BACKEND_URL}?user_id=test&question=${encodeURIComponent(
          question
        )}&selected_text=${encodeURIComponent(selectedText)}`
      );

      if (!response.body) {
        setAnswer("Error: No response body.");
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let result = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        result += decoder.decode(value);
        setAnswer(result);
      }
    } catch (error) {
      setAnswer("Network error. Backend is not reachable.");
    }
  };

  return (
    <div
      style={{
        position: "fixed",
        top: "50px",
        right: "20px",
        width: "350px",
        background: "#fff",
        border: "1px solid #ccc",
        padding: "15px",
        borderRadius: "8px",
        boxShadow: "0 0 10px rgba(0,0,0,0.2)",
        zIndex: 9999,
      }}
    >
      <h3>AI Assistant</h3>

      <p style={{ fontSize: "12px", color: "#666" }}>
        Selected text:
        <br />
        <span style={{ fontWeight: "bold" }}>
          {selectedText || "Select text from page"}
        </span>
      </p>

      <textarea
        value={question}
        placeholder="Ask something..."
        onChange={(e) => setQuestion(e.target.value)}
        style={{
          width: "100%",
          height: "70px",
          marginBottom: "10px",
          padding: "8px",
        }}
      />

      <button
        onClick={handleAsk}
        style={{
          width: "100%",
          padding: "10px",
          background: "#007bff",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
        }}
      >
        Ask
      </button>

      <div
        style={{
          marginTop: "10px",
          padding: "10px",
          background: "#f7f7f7",
          borderRadius: "5px",
          minHeight: "80px",
          whiteSpace: "pre-wrap",
        }}
      >
        <strong>Answer:</strong>
        <br />
        {answer}
      </div>
    </div>
  );
};

export default Chatbot;
