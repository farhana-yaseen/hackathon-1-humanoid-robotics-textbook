import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { apiClient } from '../services/api_client';

const TranslationButton = ({
  chapterId,
  content,
  onTranslationComplete,
  onTranslationStart,
  onTranslationError
}) => {
  const [isTranslating, setIsTranslating] = useState(false);
  const [isTranslated, setIsTranslated] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState('en'); // 'en' for English, 'ur' for Urdu
  const { user, isAuthenticated } = useAuth();

  // Load language preference from localStorage on component mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem(`translation-preference-${chapterId}`);
    if (savedLanguage) {
      setCurrentLanguage(savedLanguage);
      if (savedLanguage === 'ur') {
        setIsTranslated(true);
      }
    }
  }, [chapterId]);

  const translateToUrdu = async () => {
    if (!chapterId || !content) {
      onTranslationError && onTranslationError('No content to translate');
      return;
    }

    if (!isAuthenticated) {
      onTranslationError && onTranslationError('Please sign in to use translation feature');
      return;
    }

    setIsTranslating(true);
    onTranslationStart && onTranslationStart();

    try {
      // First, record module access
      await recordModuleAccess(chapterId);

      // Use the apiClient for translation
      const translationResult = await apiClient.translateChapter({
        chapter_id: chapterId,
        target_language: 'ur', // Translate to Urdu
        user_session_id: user?.id
      });

      onTranslationComplete(translationResult.translated_content);
      setIsTranslated(true);
      setCurrentLanguage('ur');

      // Save language preference to localStorage
      localStorage.setItem(`translation-preference-${chapterId}`, 'ur');
    } catch (error) {
      console.error('Translation error:', error);

      // Handle timeout errors specifically
      let errorMessage = error instanceof Error ? error.message : 'Translation failed';
      if (error.message && error.message.includes('timeout')) {
        errorMessage = 'Translation request timed out. Please try again.';
      }

      onTranslationError && onTranslationError(errorMessage);
    } finally {
      setIsTranslating(false);
    }
  };

  const toggleTranslation = async () => {
    if (currentLanguage === 'ur') {
      // Switch back to English (original content)
      onTranslationComplete(content); // Return original content
      setIsTranslated(false);
      setCurrentLanguage('en');

      // Save language preference to localStorage
      localStorage.setItem(`translation-preference-${chapterId}`, 'en');
    } else {
      // Translate to Urdu
      await translateToUrdu();
    }
  };

  const recordModuleAccess = async (moduleId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/auth/modules/${moduleId}/access`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: user?.id || 'anonymous',
          module_id: moduleId,
          position: 0, // For translation, we'll record position as 0
          session_id: user?.id || `anonymous_${Date.now()}`
        }),
      });

      if (!response.ok) {
        console.warn('Failed to record module access:', response.statusText);
      }
    } catch (error) {
      console.warn('Error recording module access:', error);
    }
  };

  return (
    <button
      onClick={toggleTranslation}
      disabled={isTranslating || !isAuthenticated}
      className={`
        px-4 py-2 rounded-md font-medium text-sm transition-colors
        ${!isAuthenticated
          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
          : isTranslating
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : currentLanguage === 'ur'
              ? 'bg-green-100 text-green-800 hover:bg-green-200'
              : 'bg-blue-600 text-white hover:bg-blue-700'
        }
      `}
    >
      {!isAuthenticated ? (
        <span className="flex items-center">
          <span className="mr-2">🔒</span>
          Sign In to Translate
        </span>
      ) : isTranslating ? (
        <span className="flex items-center">
          <span className="animate-spin mr-2">⏳</span>
          Processing...
        </span>
      ) : currentLanguage === 'ur' ? (
        <span className="flex items-center">
          <span className="mr-2">🇬🇧</span>
          Translate to English
        </span>
      ) : (
        <span className="flex items-center">
          <span className="mr-2">🇵🇰</span>
          Translate to Urdu
        </span>
      )}
    </button>
  );
};

export default TranslationButton;