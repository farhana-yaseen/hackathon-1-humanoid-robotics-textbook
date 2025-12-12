import React, { useState } from 'react';
import Chatbot from '../Chatbot'; // Import the existing Chatbot component

const ChatWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={toggleChat}
          className="fixed bottom-5 right-5 bg-gradient-to-r from-blue-500 via-purple-500 to-indigo-600 hover:from-blue-600 hover:via-purple-600 hover:to-indigo-700 text-white w-16 h-16 rounded-full shadow-xl flex items-center justify-center z-50 transition-all duration-300 focus:outline-none focus:ring-4 focus:ring-purple-500 focus:ring-opacity-50 hover:scale-105 active:scale-95 group"
          aria-label="Open chat"
          style={{ bottom: '20px', right: '20px' }}
        >
          <div className="flex flex-col items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <span className="text-xs font-bold">Chatbot</span>
          </div>
        </button>
      )}

      {isOpen && (
        <div className="fixed z-50" style={{ bottom: '80px', right: '20px' }}>
          <div className="w-[360px] max-w-[90vw]">
            <Chatbot isEmbedded={true} onClose={() => setIsOpen(false)} />
          </div>
        </div>
      )}
    </>
  );
};

export default ChatWidget;