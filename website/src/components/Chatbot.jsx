import React, { useState, useEffect } from "react";
import { useLocation } from "@docusaurus/router";
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../services/api_client';

const Chatbot = ({ isEmbedded = false, onClose }) => {
  // Only check for home page when not embedded
  const location = useLocation();
  const isHomePage = location.pathname === '/' || location.pathname === '/index.html';

  if (!isEmbedded && isHomePage) {
    return null;
  }

  // Function to get backend URL safely
  const getBackendURL = () => {
    // Use static default for Docusaurus
    return "http://localhost:8000/api";
  };

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [selectedText, setSelectedText] = useState("");
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [targetLanguage, setTargetLanguage] = useState(null); // null means original language
  const { user } = useAuth();

  // State for drag functionality (only when not embedded)
  const [position, setPosition] = useState({
    x: isEmbedded ? window.innerWidth - 380 : 20, // Position near the button when embedded
    y: isEmbedded ? window.innerHeight - 500 : 20 // Position near the button when embedded
  });
  const [isDragging, setIsDragging] = useState(false);
  const [dragOffset, setDragOffset] = useState({ x: 0, y: 0 });

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

  // Drag event handlers
  const handleMouseDown = (e) => {
    e.preventDefault();
    setIsDragging(true);
    const rect = e.currentTarget.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const elementWidth = 360; // Width of the chatbot container
    const elementHeight = 400; // Approximate height of the chatbot container

    let newX = e.clientX - dragOffset.x;
    let newY = e.clientY - dragOffset.y;

    // Boundary checks to keep the element within the viewport
    newX = Math.max(0, Math.min(newX, viewportWidth - elementWidth));
    newY = Math.max(0, Math.min(newY, viewportHeight - elementHeight));

    setPosition({ x: newX, y: newY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Add mouse event listeners when dragging (only when not embedded)
  useEffect(() => {
    if (!isEmbedded && isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);

      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, dragOffset.x, dragOffset.y, isEmbedded]);

  const translateResponse = async (response, targetLang) => {
    if (!targetLang || targetLang === 'English') {
      return response; // Return original if English or no target language
    }

    try {
      const result = await apiClient.translateChatbotResponse({
        text: response,
        target_language: targetLang
      });
      return result.translated_text || response;
    } catch (error) {
      console.error('Translation error:', error);
      return response; // Return original if translation fails
    }
  };

  const handleAsk = async () => {
    if (!question) {
      alert("Please type a question to ask.");
      return;
    }

    // Use selected text if available, otherwise use a default or the question context
    const contextToUse = selectedText || "General knowledge";

    // Add user message to chat
    setMessages(prev => [...prev, { type: 'user', content: question }]);
    setIsTyping(true);
    setAnswer("");

    try {
      // For now, using a direct fetch since the backend endpoint might not match the API client format
      // In a real implementation, we would use apiClient.queryRAG once the backend is properly configured
      const BACKEND_URL = getBackendURL(); // Get the backend URL safely
      // Using GET method with query parameters as the backend endpoint expects
      const response = await fetch(
        `${BACKEND_URL}/selected-chat-stream?user_id=test&question=${encodeURIComponent(question)}&selected_text=${encodeURIComponent(contextToUse)}`,
        {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      // Handle streaming response from the backend
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let result = '';

      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value);
          // Process SSE data (format: "data: {content}\n\n")
          const lines = chunk.split('\n');
          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataContent = line.slice(6); // Remove "data: " prefix
              if (dataContent.trim()) {
                result += dataContent;
              }
            }
          }
        }
      } finally {
        reader.releaseLock();
      }

      // Translate the response if a target language is selected
      const translatedResult = targetLanguage ? await translateResponse(result, targetLanguage) : result;

      setAnswer(translatedResult);

      // Store both original and translated content
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: translatedResult,
        originalContent: targetLanguage ? result : undefined
      }]);
    } catch (error) {
      console.error("Chat error:", error);
      const errorMsg = "Network error. Please make sure the backend server is running.";
      setAnswer(errorMsg);
      setMessages(prev => [...prev, { type: 'assistant', content: errorMsg }]);
    } finally {
      setIsTyping(false);
      setQuestion(""); // Clear the input after sending
    }
  };

  return (

<div
  className="chatbot-container-modern"
  style={{
    left: isEmbedded ? 'auto' : `${position.x}px`,
    top: isEmbedded ? 'auto' : `${position.y}px`,
    right: isEmbedded ? '20px' : 'auto',
    bottom: isEmbedded ? '80px' : 'auto',
    cursor: isEmbedded ? 'default' : (isDragging ? 'grabbing' : 'grab')
  }}
>
  {/* Chatbot container */}
  <div className="chatbot-container">

    {/* Header */}
    <div
      className="chatbot-header"
      onMouseDown={isEmbedded ? undefined : handleMouseDown}
    >
      <h3 className="chatbot-title">Rag Chatbot</h3>

      {isEmbedded && onClose && (
        <button
          onClick={onClose}
          className="chatbot-close"
          aria-label="Close chat"
        >
          ×
        </button>
      )}

      {/* Language dropdown */}
      <select
        value={targetLanguage || ''}
        onChange={(e) => setTargetLanguage(e.target.value || null)}
        className="chatbot-language-select"
      >
        <option value="">EN</option>
        <option value="Urdu">UR</option>
      </select>
    </div>

    {/* Messages area */}
    <div className="chatbot-messages">

      {selectedText && messages.length === 0 && (
        <div className="chatbot-selected-text">
          <p className="text-xs italic">{selectedText}</p>
        </div>
      )}

      {messages.length === 0 && !selectedText && (
        <div className="chatbot-empty-state">
          Ask anything!
        </div>
      )}

      {messages.map((msg, index) => (
        <div key={index} className={msg.type === 'user' ? 'chatbot-message-user' : 'chatbot-message-assistant'}>
          <p className="whitespace-pre-wrap">{msg.content}</p>
        </div>
      ))}

      {selectedText && messages.length > 0 && (
        <div className="chatbot-selected-text">
          <p className="text-xs italic">{selectedText}</p>
        </div>
      )}

      {isTyping && (
        <div className="chatbot-typing">
          <span>Typing...</span>
        </div>
      )}
    </div>

    {/* Input area */}
    <div className="chatbot-input-area">
      <div className="flex space-x-1">
        <input
          type="text"
          value={question}
          placeholder={selectedText ? "Ask..." : "Ask..."}
          onChange={(e) => setQuestion(e.target.value)}
          className="chatbot-input"
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              if (!isTyping && question.trim()) {
                handleAsk();
              }
            }
          }}
          disabled={isTyping}
        />
        <button
          onClick={handleAsk}
          disabled={!question.trim() || isTyping}
          className="chatbot-send-button"
        >
          Ask
        </button>
      </div>
    </div>

  </div>
</div>
);
};

export default Chatbot;