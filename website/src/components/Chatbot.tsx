import React, { useState, useEffect } from "react";
import { useLocation } from "@docusaurus/router";

// Function to safely get the backend URL, handling SSR
const getBackendURL = () => {
  if (typeof window !== 'undefined' && window.BACKEND_API_URL) {
    return (window as any).BACKEND_API_URL;
  }
  return "http://localhost:8000/api";
};

interface ChatbotProps {
  isEmbedded?: boolean;
  onClose?: () => void;
}

const Chatbot: React.FC<ChatbotProps> = ({ isEmbedded = false, onClose }) => {
  // Only check for home page when not embedded
  const location = useLocation();
  const isHomePage = location.pathname === '/' || location.pathname === '/index.html';

  if (!isEmbedded && isHomePage) {
    return null;
  }

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [selectedText, setSelectedText] = useState("");
  const [messages, setMessages] = useState<Array<{type: string, content: string}>>([]);
  const [isTyping, setIsTyping] = useState(false);
  const [isOpen, setIsOpen] = useState(false);

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
      const BACKEND_URL = getBackendURL(); // Get the backend URL safely
      const response = await fetch(
        `${BACKEND_URL}/selected-chat-stream?user_id=test&question=${encodeURIComponent(
          question
        )}&selected_text=${encodeURIComponent(contextToUse)}`
      );

      if (!response.body) {
        setAnswer("Error: No response body from server.");
        setMessages(prev => [...prev, { type: 'assistant', content: "Error: No response body from server." }]);
        setIsTyping(false);
        return;
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let result = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        // Process server-sent events
        const lines = chunk.split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6); // Remove 'data: ' prefix
            if (data.trim() !== '') {
              result += data;
              setAnswer(prev => prev + data);
            }
          }
        }
      }

      // Add assistant response to chat
      if (result) {
        setMessages(prev => [...prev, { type: 'assistant', content: result }]);
      }
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
    className="fixed z-[99999] w-[360px] max-w-[90vw] bg-white"
    style={{
      left: isEmbedded ? 'auto' : `${position.x}px`,
      top: isEmbedded ? 'auto' : `${position.y}px`,
      right: isEmbedded ? '20px' : 'auto',
      bottom: isEmbedded ? '80px' : 'auto',
      cursor: isEmbedded ? 'default' : (isDragging ? 'grabbing' : 'grab')
    }}
  >
    {/* Chatbot container */}
    <div className="bg-gradient-to-br from-white to-gray-100 rounded-2xl shadow-2xl border border-gray-300 overflow-hidden transition-all duration-300 flex flex-col h-[65vh] max-h-[75vh]">

      {/* Header */}
      <div
        className={`bg-gradient-to-r from-indigo-600 to-purple-700 p-4 text-white flex items-center justify-between shadow-lg ${isEmbedded ? '' : 'cursor-move'}`}
        onMouseDown={isEmbedded ? undefined : handleMouseDown}
      >
        <h3 className="font-bold text-base flex items-center">
          <div className="relative mr-2">
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-ping"></div>
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
          </div>
          <span>AI Assistant</span>
        </h3>
        {isEmbedded && onClose && (
          <button
            onClick={onClose}
            className="text-white hover:text-gray-200 focus:outline-none transition-colors duration-200"
            aria-label="Close chat"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        )}
      </div>

      {/* Chat messages container */}
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4">

        {selectedText && messages.length === 0 && (
          <div className="flex justify-start">
            <div className="bg-indigo-100 text-gray-800 p-3 rounded-lg max-w-[85%] shadow-sm">
              <p className="text-sm font-medium mb-1">Selected Context:</p>
              <p className="text-sm">{selectedText}</p>
            </div>
          </div>
        )}

        {messages.length === 0 && !selectedText && (
          <div className="text-center py-8">
            <div className="inline-block p-4 bg-indigo-50 rounded-lg border border-indigo-200 shadow-sm">
              <p className="text-sm text-indigo-700">
                <span className="font-medium">Tip:</span> Ask anything! Select text on the page for context.
              </p>
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`p-3 rounded-lg max-w-[85%] shadow-sm ${
              msg.type === 'user'
                ? 'bg-indigo-600 text-white rounded-tr-none'
                : 'bg-gray-200 text-gray-800 rounded-tl-none'
            }`}>
              <p className="text-sm whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}

        {/* Show selected text context when user asks with selected text */}
        {selectedText && messages.length > 0 && (
          <div className="flex justify-start animate-fadeIn">
            <div className="bg-yellow-100 text-gray-800 p-3 rounded-lg max-w-[85%] shadow border-l-4 border-yellow-500">
              <p className="text-sm font-medium mb-1">Context from selected text:</p>
              <p className="text-sm italic">{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}</p>
            </div>
          </div>
        )}

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-[85%] shadow">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input area */}
      <div className="border-t border-gray-300 p-2 bg-white">
        <div className="flex space-x-2">
          <input
            type="text"
            value={question}
            placeholder={selectedText ? "Ask about selected text..." : "Ask anything..."}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all bg-white"
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
            className={`px-2 py-2 rounded-lg font-medium text-white transition-all duration-300 text-sm shadow ${
              !question.trim() || isTyping
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {isTyping ? "..." : "Send"}
          </button>
        </div>
      </div>

    </div>
  </div>





































    // <div className="fixed bottom-5 right-5 z-[9999] w-96 max-w-[90vw]">
    //   {/* Chatbot container - ChatGPT-like interface */}
    //   <div className="bg-white rounded-xl shadow-2xl border border-gray-300 overflow-hidden transition-all duration-300 flex flex-col h-[65vh] max-h-[75vh]">
    //     {/* Header */}
    //     <div className="bg-gradient-to-r from-blue-600 to-purple-700 p-4 text-white flex items-center justify-between">
    //       <h3 className="font-bold text-base flex items-center">
    //         <div className="relative mr-2">
    //           <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-400 rounded-full animate-ping"></div>
    //           <div className="w-2 h-2 bg-green-500 rounded-full"></div>
    //         </div>
    //         <span>AI Assistant</span>
    //       </h3>
    //     </div>

    //     {/* Chat messages container */}
    //     <div className="flex-1 overflow-y-auto p-4 bg-gray-50 space-y-4">
    //       {/* Show selected text as context if available */}
    //       {selectedText && messages.length === 0 && (
    //         <div className="flex justify-start">
    //           <div className="bg-blue-100 text-gray-800 p-3 rounded-lg max-w-[85%]">
    //             <p className="text-sm font-medium mb-1">Selected Context:</p>
    //             <p className="text-sm">{selectedText}</p>
    //           </div>
    //         </div>
    //       )}

    //       {/* Welcome message when no messages exist */}
    //       {messages.length === 0 && !selectedText && (
    //         <div className="text-center py-8">
    //           <div className="inline-block p-4 bg-blue-50 rounded-lg border border-blue-200">
    //             <p className="text-sm text-blue-700">
    //               <span className="font-medium">Tip:</span> Ask anything! Select text on the page for context.
    //             </p>
    //           </div>
    //         </div>
    //       )}

    //       {/* Render chat messages */}
    //       {messages.map((msg, index) => (
    //         <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
    //           <div className={`p-3 rounded-lg max-w-[85%] ${
    //             msg.type === 'user'
    //               ? 'bg-blue-500 text-white'
    //               : 'bg-gray-200 text-gray-800'
    //           }`}>
    //             <p className="text-sm">{msg.content}</p>
    //           </div>
    //         </div>
    //       ))}

    //       {/* Typing indicator */}
    //       {isTyping && (
    //         <div className="flex justify-start">
    //           <div className="bg-gray-200 text-gray-800 p-3 rounded-lg max-w-[85%]">
    //             <div className="flex space-x-1">
    //               <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
    //               <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
    //               <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
    //             </div>
    //           </div>
    //         </div>
    //       )}
    //     </div>

    //     {/* Input area */}
    //     <div className="border-t border-gray-300 p-3 bg-white">
    //       <div className="flex space-x-2">
    //         <input
    //           type="text"
    //           value={question}
    //           placeholder={selectedText ? "Ask about selected text..." : "Ask anything..."}
    //           onChange={(e) => setQuestion(e.target.value)}
    //           className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all bg-white"
    //           onKeyPress={(e) => {
    //             if (e.key === 'Enter' && !e.shiftKey) {
    //               e.preventDefault();
    //               if (!isTyping && question.trim()) {
    //                 handleAsk();
    //               }
    //             }
    //           }}
    //           disabled={isTyping}
    //         />
    //         <button
    //           onClick={handleAsk}
    //           disabled={!question.trim() || isTyping}
    //           className={`px-4 py-2 rounded-lg font-medium text-white transition-all duration-300 text-sm ${
    //             !question.trim() || isTyping
    //               ? "bg-gray-400 cursor-not-allowed"
    //               : "bg-blue-600 hover:bg-blue-700"
    //           }`}
    //         >
    //           {isTyping ? "..." : "Send"}
    //         </button>
    //       </div>
    //     </div>
    //   </div>
    // </div>
  );
  
};

export default Chatbot;

