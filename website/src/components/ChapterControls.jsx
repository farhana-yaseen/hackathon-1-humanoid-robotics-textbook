import React from 'react';
import { useSession } from '../auth/betterAuthClient';
import TranslationButton from './TranslationButton';

export default function ChapterControls({
  chapterId,
  content,
  onPersonalizeClick,
  onTranslationComplete,
  onTranslationStart,
  onTranslationError,
}) {
  const { data: session, status } = useSession();

  // Only show controls to logged-in users
  if (status !== 'authenticated') {
    return null;
  }

  return (
    <div className="chapter-controls flex gap-3 mb-6 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border border-indigo-100">
      <button
        onClick={onPersonalizeClick}
        className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white font-medium rounded-lg shadow-md transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        Personalize
      </button>

      <TranslationButton
        chapterId={chapterId}
        content={content}
        onTranslationComplete={onTranslationComplete}
        onTranslationStart={onTranslationStart}
        onTranslationError={onTranslationError}
      />
    </div>
  );
}