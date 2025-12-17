import React, { useState } from 'react';
import Chatbot from '../Chatbot'; // Import the existing Chatbot component

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="chatbot-button bg-blue-500 text-white w-12 h-12 rounded-full shadow-md flex items-center justify-center transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-blue-300 hover:scale-105"
          aria-label="Open chat"
          style={{
            width: '48px',
            height: '48px',
            borderRadius: '50%',
            background: '#3b82f6',
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
            transition: 'all 0.2s ease'
          }}
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ width: '20px', height: '20px' }}>
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
        </button>
      )}

      {isOpen && (
        <div className="chatbot-container">
          <div className="w-[360px] max-w-[90vw]">
            <Chatbot isEmbedded={true} onClose={() => setIsOpen(false)} />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;