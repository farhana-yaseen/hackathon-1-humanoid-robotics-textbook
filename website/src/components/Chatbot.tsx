import React, { useState, useEffect } from "react";
import { useLocation } from "@docusaurus/router";
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../services/api_client';

// Define the props type
type ChatbotProps = {
  isEmbedded?: boolean;
  onClose?: () => void;
};

const Chatbot: React.FC<ChatbotProps> = ({ isEmbedded = false, onClose }) => {
  // Only check for home page when not embedded
  const location = useLocation();
  const isHomePage = location.pathname === '/' || location.pathname === '/index.html';

  if (!isEmbedded && isHomePage) {
    return null;
  }

  // Function to get backend URL safely
  const getBackendURL = (): string => {
    // Use static default for Docusaurus
    return "http://localhost:8000/api";
  };

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [selectedText, setSelectedText] = useState("");
  const [messages, setMessages] = useState<Array<{type: string, content: string, originalContent?: string}>>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [targetLanguage, setTargetLanguage] = useState<string | null>(null); // null means original language
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
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsDragging(true);
    const rect = e.currentTarget.getBoundingClientRect();
    setDragOffset({
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    });
  };

  const handleMouseMove = (e: MouseEvent) => {
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

  const translateResponse = async (response: string, targetLang: string): Promise<string> => {
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
      const response = await fetch(
        `${BACKEND_URL}/selected-chat-stream`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: 'test',
            question: question,
            selected_text: contextToUse
          })
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      const result = data.answer || data.message || "No response received";

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
  className="fixed z-[99999] w-[320px] max-w-[90vw] max-h-[60vh]"
  style={{
    left: isEmbedded ? 'auto' : `${position.x}px`,
    top: isEmbedded ? 'auto' : `${position.y}px`,
    right: isEmbedded ? '20px' : 'auto',
    bottom: isEmbedded ? '80px' : 'auto',
    cursor: isEmbedded ? 'default' : (isDragging ? 'grabbing' : 'grab')
  }}
>
  {/* Chatbot container */}
  <div className="bg-white rounded-lg shadow-lg border border-gray-300 overflow-hidden transition-all duration-300 flex flex-col h-auto max-h-[60vh]">


    {/* Header */}
    <div
      className={`bg-gray-100 p-2 text-gray-800 flex items-center justify-between ${isEmbedded ? '' : 'cursor-move'}`}
      onMouseDown={isEmbedded ? undefined : handleMouseDown}
    >
      <h3 className="font-semibold text-sm flex items-center">
        <span className="flex items-center">
          Chat
        </span>
      </h3>
      <div className="flex items-center space-x-1">
        {/* Language selection dropdown - smaller */}
        <select
          value={targetLanguage || ''}
          onChange={(e) => setTargetLanguage(e.target.value || null)}
          className="bg-gray-200 text-gray-700 text-xs rounded px-1 py-0.5 border border-gray-400 focus:outline-none focus:ring-1 focus:ring-gray-500"
        >
          <option value="">EN</option>
          <option value="Urdu">UR</option>
        </select>
        {isEmbedded && onClose && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 focus:outline-none transition-colors duration-200 p-1 rounded hover:bg-gray-200"
            aria-label="Close chat"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>
    </div>

    {/* Chat messages container */}
    <div className="flex-1 overflow-y-auto p-2 bg-white space-y-2 max-h-40">

      {selectedText && messages.length === 0 && (
        <div className="flex justify-start">
          <div className="bg-blue-50 text-gray-700 p-2 rounded-lg max-w-[85%] text-xs">
            <p className="text-xs italic">{selectedText.substring(0, 80)}{selectedText.length > 80 ? '...' : ''}</p>
          </div>
        </div>
      )}

      {messages.length === 0 && !selectedText && (
        <div className="text-center py-3 text-xs text-gray-500">
          Ask anything!
        </div>
      )}

      {messages.map((msg, index) => (
        <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
          <div className={`p-2 rounded-lg text-xs ${
            msg.type === 'user'
              ? 'bg-blue-500 text-white rounded-tr-sm'
              : 'bg-gray-100 text-gray-800 rounded-tl-sm'
          }`}>
            <p className="whitespace-pre-wrap">{msg.content}</p>
          </div>
        </div>
      ))}

      {/* Show selected text context when user asks with selected text */}
      {selectedText && messages.length > 0 && (
        <div className="flex justify-start">
          <div className="bg-amber-50 text-gray-700 p-2 rounded-lg max-w-[85%] text-xs">
            <p className="text-xs italic">{selectedText.substring(0, 80)}{selectedText.length > 80 ? '...' : ''}</p>
          </div>
        </div>
      )}

      {isTyping && (
        <div className="flex justify-start">
          <div className="bg-gray-100 text-gray-800 p-2 rounded-lg text-xs">
            <span className="text-xs text-gray-500">Typing...</span>
          </div>
        </div>
      )}
    </div>

    {/* Input area */}
    <div className="border-t border-gray-200 p-2 bg-white">
      <div className="flex space-x-1">
        <input
          type="text"
          value={question}
          placeholder={selectedText ? "Ask..." : "Ask..."}
          onChange={(e) => setQuestion(e.target.value)}
          className="flex-1 px-2 py-1 text-xs border border-gray-300 rounded focus:ring-1 focus:ring-blue-500 focus:border-blue-500 bg-gray-50 focus:bg-white"
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
          className={`px-2 py-1 rounded text-white transition-all duration-300 text-xs ${
            !question.trim() || isTyping
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600"
          }`}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>

  </div>
</div>

);
};

export default Chatbot;