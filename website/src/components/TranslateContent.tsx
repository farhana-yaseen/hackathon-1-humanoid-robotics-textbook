import React, { useState, useEffect } from 'react';
import { useSession } from '../auth/betterAuthClient';

interface TranslateContentProps {
  chapterTitle: string;
  chapterContent: string;
}

const TranslateContent: React.FC<TranslateContentProps> = ({ chapterTitle, chapterContent }) => {
  const { data: session, status } = useSession();
  const [isTranslated, setIsTranslated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [translatedContent, setTranslatedContent] = useState('');
  const [showOptions, setShowOptions] = useState(false);

  const handleTranslate = async () => {
    if (!session) {
      alert('Please sign in to translate content');
      return;
    }

    setIsLoading(true);

    try {
      const translatedContentResult = await translateContentToUrduWithBackend(
        chapterContent,
        chapterTitle
      );

      setTranslatedContent(translatedContentResult);
      setIsTranslated(true);
    } catch (error) {
      console.error('Error translating content:', error);
      alert('Error translating content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const translateContentToUrduWithBackend = async (
    content: string,
    title: string
  ): Promise<string> => {
    const response = await fetch(`${(typeof window !== 'undefined' && (window as any).BACKEND_API_URL) || 'http://localhost:8000'}/api/translate-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chapter_title: title,
        chapter_content: content,
        target_language: 'ur'
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to translate content');
    }

    const data = await response.json();
    return data.translated_content;
  };

  const handleReset = () => {
    setTranslatedContent('');
    setIsTranslated(false);
  };

  if (status === 'loading') {
    return (
      <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
        <div className="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed">Loading translation...</div>
      </div>
    );
  }

  if (status !== 'authenticated') {
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
        {!isTranslated ? (
          <button
            className={`px-4 py-2 rounded text-white font-medium transition-colors ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-orange-500 hover:bg-orange-600'
            }`}
            onClick={handleTranslate}
            disabled={isLoading}
          >
            {isLoading ? 'Translating to Urdu...' : 'Translate to Urdu'}
          </button>
        ) : (
          <button
            className="px-4 py-2 bg-red-500 text-white rounded font-medium hover:bg-red-600 transition-colors"
            onClick={handleReset}
          >
            Reset to Original
          </button>
        )}

        <button
          className="px-4 py-2 bg-blue-500 text-white rounded font-medium hover:bg-blue-600 transition-colors"
          onClick={() => setShowOptions(!showOptions)}
        >
          {showOptions ? 'Hide Details' : 'Show Translation Info'}
        </button>
      </div>

      {showOptions && (
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded">
          <h4 className="text-lg font-semibold text-gray-800 mb-2">Urdu Translation Information</h4>
          <p className="mb-2 text-gray-700">This feature uses AI to translate the content to Urdu while preserving the educational value and technical accuracy of the original text.</p>
          <p className="text-gray-700">Translation quality may vary for highly technical terms. The original English content is always available using the "Reset to Original" button.</p>
        </div>
      )}

      {isTranslated && translatedContent && (
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded">
          <h4 className="text-lg font-semibold text-gray-800 mb-2">Translated Content (اردو ترجمہ)</h4>
          <div className="leading-relaxed" dir="ltr">
            {translatedContent.split('\n').map((line, i) => (
              line.startsWith('**') && line.endsWith('**') ? (
                <h5 key={i} className="text-gray-800 my-2 font-semibold">{line.substring(2, line.length - 2)}</h5>
              ) : line.startsWith('**') && line.includes(':') ? (
                <p key={i} className="text-gray-600 my-2 italic">{line.substring(2, line.length - 2)}</p>
              ) : (
                <p key={i} className="my-2" dir="ltr">{line}</p>
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslateContent;