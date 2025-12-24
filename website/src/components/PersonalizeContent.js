import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { userBackgroundService } from '../services/userBackground';

const PersonalizeContent = ({ chapterTitle, chapterContent }) => {
  const { user, isAuthenticated, loading } = useAuth();
  const [isPersonalized, setIsPersonalized] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [userBackground, setUserBackground] = useState(null);
  const [personalizedContent, setPersonalizedContent] = useState('');
  const [showOptions, setShowOptions] = useState(false);

  // Load user background when user is available
  useEffect(() => {
    const loadUserBackground = async () => {
      if (user?.id) {
        const background = await userBackgroundService.getUserBackground(user.id);
        setUserBackground(background);
      }
    };

    if (isAuthenticated) {
      loadUserBackground();
    }
  }, [user, isAuthenticated]);

  const handlePersonalize = async () => {
    if (!isAuthenticated) {
      alert('Please sign in to personalize content');
      return;
    }

    if (!userBackground) {
      alert('Please complete your profile to enable personalization');
      window.location.href = '/auth/signup'; // or profile page
      return;
    }

    setIsLoading(true);

    try {
      const personalizedContentResult = await personalizeContentWithBackend(
        chapterContent,
        userBackground,
        chapterTitle
      );

      setPersonalizedContent(personalizedContentResult);
      setIsPersonalized(true);
    } catch (error) {
      console.error('Error personalizing content:', error);
      alert('Error personalizing content. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const personalizeContentWithBackend = async (
    content,
    background,
    title
  ) => {
    const response = await fetch(`${(typeof window !== 'undefined' && window.BACKEND_API_URL) || 'http://localhost:8000'}/api/personalize-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chapter_title: title,
        chapter_content: content,
        user_background: {
          software_experience: background.softwareExperience,
          hardware_experience: background.hardwareExperience,
          robotics_experience: background.roboticsExperience,
          programming_languages: background.programmingLanguages || [],
          hardware_platforms: background.hardwarePlatforms || [],
          years_of_experience: background.yearsOfExperience,
          primary_interest: background.primaryInterest,
          education_level: background.educationLevel
        }
      }),
    });

    if (!response.ok) {
      throw new Error('Failed to personalize content');
    }

    const data = await response.json();
    return data.personalized_content;
  };

  const handleReset = () => {
    setPersonalizedContent('');
    setIsPersonalized(false);
  };

  if (loading) {
    return (
      <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
        <div className="bg-gray-400 text-white px-4 py-2 rounded cursor-not-allowed">Loading personalization...</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50 text-center">
        <div>
          <p className="mb-4">Sign in to personalize this content to your experience level</p>
          <a href="/auth/signin" className="button button--primary">Sign In</a>
        </div>
      </div>
    );
  }

  return (
    <div className="mt-8 p-6 border border-gray-200 rounded-lg bg-gray-50">
      <div className="flex gap-4 mb-4 flex-wrap">
        {!isPersonalized ? (
          <button
            className={`px-4 py-2 rounded text-white font-medium transition-colors ${
              isLoading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-green-500 hover:bg-green-600'
            }`}
            onClick={handlePersonalize}
            disabled={isLoading}
          >
            {isLoading ? 'Personalizing...' : 'Personalize Content'}
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
          {showOptions ? 'Hide Details' : 'Show My Profile'}
        </button>
      </div>

      {showOptions && userBackground && (
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded">
          <h4 className="text-lg font-semibold text-gray-800 mb-2">Your Profile for Personalization</h4>
          <ul className="list-disc pl-5 space-y-1">
            {userBackground.softwareExperience && (
              <li><strong>Software Experience:</strong> {userBackground.softwareExperience}</li>
            )}
            {userBackground.hardwareExperience && (
              <li><strong>Hardware Experience:</strong> {userBackground.hardwareExperience}</li>
            )}
            {userBackground.roboticsExperience && (
              <li><strong>Robotics Experience:</strong> {userBackground.roboticsExperience}</li>
            )}
            {userBackground.programmingLanguages && userBackground.programmingLanguages.length > 0 && (
              <li><strong>Programming Languages:</strong> {userBackground.programmingLanguages.join(', ')}</li>
            )}
            {userBackground.hardwarePlatforms && userBackground.hardwarePlatforms.length > 0 && (
              <li><strong>Hardware Platforms:</strong> {userBackground.hardwarePlatforms.join(', ')}</li>
            )}
            {userBackground.yearsOfExperience && (
              <li><strong>Years of Experience:</strong> {userBackground.yearsOfExperience}</li>
            )}
            {userBackground.primaryInterest && (
              <li><strong>Primary Interest:</strong> {userBackground.primaryInterest}</li>
            )}
            {userBackground.educationLevel && (
              <li><strong>Education Level:</strong> {userBackground.educationLevel}</li>
            )}
          </ul>
        </div>
      )}

      {isPersonalized && personalizedContent && (
        <div className="mt-4 p-4 bg-white border border-gray-300 rounded">
          <h4 className="text-lg font-semibold text-gray-800 mb-2">Personalized Content Preview</h4>
          <div className="leading-relaxed">
            {personalizedContent.split('\n').map((line, i) => (
              line.startsWith('> **') ? (
                <blockquote key={i} className="my-2 pl-4 border-l-4 border-green-500 bg-green-50 p-2 italic">{line.substring(2)}</blockquote>
              ) : (
                <p key={i}>{line}</p>
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalizeContent;