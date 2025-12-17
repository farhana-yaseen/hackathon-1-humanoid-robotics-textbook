import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';

const TranslationButton = ({
  chapterId,
  content,
  onTranslationComplete,
  onTranslationStart,
  onTranslationError
}) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [targetLanguage, setTargetLanguage] = useState('Urdu');
  const { user } = useAuth();

  const translateContent = async () => {
    if (!chapterId || !content) {
      onTranslationError && onTranslationError('No content to translate');
      return;
    }

    setIsTranslating(true);
    onTranslationStart && onTranslationStart();

    try {
      // Get user session ID or use anonymous session
      const userSessionId = user?.user_id || `anonymous_${Date.now()}`;

      // Call the backend translation API
      const response = await fetch(`/api/v1/translation/chapters/${chapterId}/translate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chapter_id: chapterId,
          target_language: targetLanguage,
          user_session_id: userSessionId
        }),
      });

      if (!response.ok) {
        throw new Error(`Translation failed: ${response.statusText}`);
      }

      const data = await response.json();
      onTranslationComplete(data.translated_content);
      setIsTranslated(true);
    } catch (error) {
      console.error('Translation error:', error);
      onTranslationError && onTranslationError(error instanceof Error ? error.message : 'Translation failed');
    } finally {
      setIsTranslating(false);
    }
  };

  const toggleTranslation = () => {
    if (isTranslated) {
      // Reset to original content
      onTranslationComplete(content);
      setIsTranslated(false);
    } else {
      // Start translation
      translateContent();
    }
  };

  return (
    <button
      onClick={toggleTranslation}
      disabled={isTranslating}
      className={`
        px-4 py-2 rounded-md font-medium text-sm transition-colors
        ${isTranslating
          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
          : isTranslated
            ? 'bg-green-100 text-green-800 hover:bg-green-200'
            : 'bg-blue-600 text-white hover:bg-blue-700'
        }
      `}
    >
      {isTranslating ? (
        <span className="flex items-center">
          <span className="animate-spin mr-2">⏳</span>
          Translating...
        </span>
      ) : isTranslated ? (
        <span className="flex items-center">
          <span className="mr-2">✅</span>
          Urdu ({targetLanguage})
        </span>
      ) : (
        <span className="flex items-center">
          <span className="mr-2">🔄</span>
          Translate to Urdu
        </span>
      )}
    </button>
  );
};

export default TranslationButton;