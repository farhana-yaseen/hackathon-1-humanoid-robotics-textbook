import React, { useState, useEffect } from 'react';
import { useSession } from '../auth/betterAuthClient';

const TranslateContent = ({ chapterTitle, chapterContent }) => {
  const { data: session, status } = useSession();
  const [isTranslated, setIsTranslated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [translatedContent, setTranslatedContent] = useState('');
  const [showOptions, setShowOptions] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState('en'); // 'en' for English, 'ur' for Urdu
  const [error, setError] = useState(null);

  // Load language preference from localStorage on component mount
  useEffect(() => {
    const savedLanguage = localStorage.getItem(`translation-preference-${chapterTitle}`);
    if (savedLanguage) {
      setCurrentLanguage(savedLanguage);
      if (savedLanguage === 'ur') {
        setIsTranslated(true);
      }
    }
  }, [chapterTitle]);

  const handleTranslate = async () => {
    if (!session) {
      setError('Please sign in to translate content');
      return;
    }

    setIsLoading(true);
    setError(null); // Clear any previous errors

    try {
      // Extract module/chapter ID from the title or content for tracking
      const moduleId = extractModuleId(chapterTitle);

      // Record module access before translation
      await recordModuleAccess(moduleId);

      const translatedContentResult = await translateContentToUrduWithBackend(
        chapterContent,
        chapterTitle
      );

      setTranslatedContent(translatedContentResult);
      setIsTranslated(true);
      setCurrentLanguage('ur');

      // Save language preference to localStorage
      localStorage.setItem(`translation-preference-${chapterTitle}`, 'ur');
    } catch (error) {
      console.error('Error translating content:', error);
      setError(error.message || 'Error translating content. Please try again.');
      // Don't switch language if there's an error, keep original content visible
      setCurrentLanguage('en');
      setIsTranslated(false);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleLanguage = async () => {
    if (currentLanguage === 'ur') {
      // Switch back to English
      setCurrentLanguage('en');
      setIsTranslated(false);
      // Save language preference to localStorage
      localStorage.setItem(`translation-preference-${chapterTitle}`, 'en');
    } else {
      // Translate to Urdu
      await handleTranslate();
    }
  };

  const handleReset = () => {
    setTranslatedContent('');
    setIsTranslated(false); 
    setCurrentLanguage('en');
    // Save language preference to localStorage
    localStorage.setItem(`translation-preference-${chapterTitle}`, 'en');
  };

  const extractModuleId = (title) => {
    // Extract module ID from title (e.g., if title is "Module 1: Introduction" return "module-1")
    if (title) {
      const match = title.match(/(Module\s+\d+|Chapter\s+\d+|Lesson\s+\d+)/i);
      if (match) {
        return match[0].toLowerCase().replace(/\s+/g, '-');
      }
      return title.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
    }
    return 'unknown-module';
  };

  const recordModuleAccess = async (moduleId) => {
    try {
      const response = await fetch(`${(typeof window !== 'undefined' && window.BACKEND_API_URL) || 'http://localhost:8000'}/api/auth/modules/${moduleId}/access`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: session?.user?.id || 'anonymous',
          module_id: moduleId,
          position: 0, // For translation, we'll record position as 0
          session_id: session?.user?.id || `anonymous_${Date.now()}`
        }),
      });

      if (!response.ok) {
        console.warn('Failed to record module access:', response.statusText);
      }
    } catch (error) {
      console.warn('Error recording module access:', error);
    }
  };

  const translateContentToUrduWithBackend = async (
    content,
    title
  ) => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 35000); // 35 seconds timeout (slightly more than backend timeout)

    try {
      const response = await fetch(`${(typeof window !== 'undefined' && window.BACKEND_API_URL) || 'http://localhost:8000'}/api/translate-content`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          chapter_title: title,
          chapter_content: content,
          target_language: 'ur'
        }),
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        if (response.status === 408) {
          throw new Error('Translation request timed out. Please try again.');
        } else {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.detail || `Translation failed with status ${response.status}`);
        }
      }

      const data = await response.json();
      return data.translated_content;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error.name === 'AbortError') {
        throw new Error('Translation request timed out. Please try again.');
      }

      throw error;
    }
  };

  // More robust authentication check - Better Auth should return proper status values
  const isAuthenticated = status === 'authenticated' || (status === undefined && session && session.user);
  const isLoadingStatus = status === 'loading';

  if (isLoadingStatus) {
    return (
      <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
        <div className="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed">Loading translation...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50 text-center">
        <div>
          <p className="mb-4">Sign in to translate this content to Urdu</p>
          <a href="/auth/signin" className="button button--primary">Sign In</a>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <div className="flex gap-4 mb-4 flex-wrap">
        <button
          className={'px-4 py-2 rounded text-white font-medium transition-colors ' +
            (isLoading
              ? 'bg-gray-400 cursor-not-allowed'
              : currentLanguage === 'ur'
                ? 'bg-red-500 hover:bg-red-600' // Red for translate back to English
                : 'bg-orange-500 hover:bg-orange-600' // Orange for translate to Urdu
            )}
          onClick={handleToggleLanguage}
          disabled={isLoading}
        >
          {isLoading
            ? 'Processing...'
            : currentLanguage === 'ur'
              ? 'Translate to English'  // Button to switch back to English
              : 'Translate to Urdu'     // Button to translate to Urdu
          }
        </button>

        <button
          className="px-4 py-2 bg-blue-500 text-white rounded font-medium hover:bg-blue-600 transition-colors"
          onClick={() => setShowOptions(!showOptions)}
        >
          {showOptions ? 'Hide Details' : 'Show Translation Info'}
        </button>
      </div>

      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-300 text-red-700 rounded">
          <div className="flex items-start">
            <span className="mr-2">⚠️</span>
            <div>
              <strong>Error:</strong> {error}
              <p className="mt-1 text-sm">The original content is still visible below.</p>
            </div>
          </div>
        </div>
      )}

      {showOptions && (
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded">
          <h4 className="text-lg font-semibold text-gray-800 mb-2">Translation Information</h4>
          <p className="mb-2 text-gray-700">This feature uses AI to translate the content while preserving the educational value and technical accuracy of the original text.</p>
          <p className="text-gray-700">Translation quality may vary for highly technical terms. You can switch between languages using the toggle button above.</p>
        </div>
      )}

      {currentLanguage === 'ur' && isTranslated && translatedContent ? (
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded" dir="rtl">
          <h4 className="text-lg font-semibold text-gray-800 mb-2" dir="ltr">Translated Content (اردو ترجمہ)</h4>
          <div className="leading-relaxed text-right" dir="rtl">
            {translatedContent.split('\n').map((line, i) => {
              // Check for different formatting patterns
              if (line.trim().startsWith('# ')) {
                // H1 header
                return <h1 key={i} className="text-2xl font-bold text-gray-800 my-3 text-right" dir="rtl">{line.substring(2)}</h1>;
              } else if (line.trim().startsWith('## ')) {
                // H2 header
                return <h2 key={i} className="text-xl font-semibold text-gray-800 my-2 text-right" dir="rtl">{line.substring(3)}</h2>;
              } else if (line.trim().startsWith('### ')) {
                // H3 header
                return <h3 key={i} className="text-lg font-medium text-gray-800 my-2 text-right" dir="rtl">{line.substring(4)}</h3>;
              } else if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
                // Bold text
                return <p key={i} className="font-bold text-gray-800 my-2 text-right" dir="rtl">{line.substring(2, line.length - 2)}</p>;
              } else if (line.trim().startsWith('* ') || line.trim().startsWith('- ')) {
                // List item
                return <li key={i} className="my-1 text-right" dir="rtl">{line.substring(2)}</li>;
              } else if (line.trim().match(/^\d+\.\s/)) {
                // Numbered list item
                return <li key={i} className="my-1 text-right list-decimal" dir="rtl">{line.replace(/^\d+\.\s/, '')}</li>;
              } else if (line.trim() === '') {
                // Empty line
                return <div key={i} className="my-2"></div>;
              } else {
                // Regular paragraph
                return <p key={i} className="my-2 text-right" dir="rtl">{line}</p>;
              }
            })}
          </div>
        </div>
      ) : (
        // Show original content when not translated or when there's an error
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded" dir="ltr">
          <h4 className="text-lg font-semibold text-gray-800 mb-2">Original Content (English)</h4>
          <div className="leading-relaxed text-left" dir="ltr">
            {chapterContent.split('\n').map((line, i) => {
              // Check for different formatting patterns
              if (line.trim().startsWith('# ')) {
                // H1 header
                return <h1 key={i} className="text-2xl font-bold text-gray-800 my-3 text-left">{line.substring(2)}</h1>;
              } else if (line.trim().startsWith('## ')) {
                // H2 header
                return <h2 key={i} className="text-xl font-semibold text-gray-800 my-2 text-left">{line.substring(3)}</h2>;
              } else if (line.trim().startsWith('### ')) {
                // H3 header
                return <h3 key={i} className="text-lg font-medium text-gray-800 my-2 text-left">{line.substring(4)}</h3>;
              } else if (line.trim().startsWith('**') && line.trim().endsWith('**')) {
                // Bold text
                return <p key={i} className="font-bold text-gray-800 my-2 text-left">{line.substring(2, line.length - 2)}</p>;
              } else if (line.trim().startsWith('* ') || line.trim().startsWith('- ')) {
                // List item
                return <li key={i} className="my-1 text-left">{line.substring(2)}</li>;
              } else if (line.trim().match(/^\d+\.\s/)) {
                // Numbered list item
                return <li key={i} className="my-1 text-left list-decimal">{line.replace(/^\d+\.\s/, '')}</li>;
              } else if (line.trim() === '') {
                // Empty line
                return <div key={i} className="my-2"></div>;
              } else {
                // Regular paragraph
                return <p key={i} className="my-2 text-left">{line}</p>;
              }
            })}
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslateContent;