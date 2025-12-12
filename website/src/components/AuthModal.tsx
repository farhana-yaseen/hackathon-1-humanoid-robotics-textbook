import React, { useState } from 'react';
import { signIn, signUp } from '../auth/betterAuthClient';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  mode: 'signin' | 'signup';
  onModeChange: (mode: 'signin' | 'signup') => void;
}

const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, mode, onModeChange }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Background information states (for signup only)
  const [background, setBackground] = useState({
    roboticsExperience: '',
    programmingLanguages: '',
  });

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      if (mode === 'signup') {
        if (password !== confirmPassword) {
          setError('Passwords do not match');
          setIsSubmitting(false);
          return;
        }

        // First, create the account with Better Auth
        try {
          const authResponse = await signUp.email({
            email,
            password,
            name: email.split('@')[0], // Use part of email as name
          });

          if (authResponse?.error) {
            throw new Error(authResponse.error.message);
          }

          // After successful signup, save the background information to our Node.js auth service
          // Use a more flexible approach to handle different environments
          try {
            const BACKEND_URL = process.env.BACKEND_API_URL || 'http://localhost:3002';
            const backgroundResponse = await fetch(`${BACKEND_URL}/api/signup-background`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                email,
                background: {
                  roboticsExperience: background.roboticsExperience,
                  programmingLanguages: background.programmingLanguages,
                }
              }),
            });

            const backgroundData = await backgroundResponse.json();

            if (!backgroundResponse.ok) {
              console.warn('Background info not saved:', backgroundData.error);
              // Don't fail the signup if background info fails to save
            }
          } catch (backgroundError) {
            console.warn('Background info service unavailable:', backgroundError);
            // Don't fail the signup if background service is unavailable
          }

          alert('Account created successfully!');
          // Close the modal after successful signup
          onClose();
        } catch (authError: any) {
          console.error('Auth signup error:', authError);
          // Provide more helpful error message for common issues
          let errorMessage = authError.message || 'An error occurred during signup';

          // Check if it's a network error related to fetching
          if (authError.message?.includes('Failed to fetch') || authError.message?.includes('NetworkError')) {
            errorMessage = 'Authentication service is not available. Please make sure the backend server is running on port 3002.';
          }

          setError(errorMessage);
        }
      } else {
        try {
          const response = await signIn.email({
            email,
            password,
            callbackURL: '/', // Redirect to home page after successful login
          });

          if (response?.error) {
            throw new Error(response.error.message);
          }

          alert('Signed in successfully!');
          // Close the modal after successful sign in
          onClose();
        } catch (authError: any) {
          console.error('Auth sign in error:', authError);
          // Provide more helpful error message for common issues
          let errorMessage = authError.message || 'An error occurred during sign in';

          // Check if it's a network error related to fetching
          if (authError.message?.includes('Failed to fetch') || authError.message?.includes('NetworkError')) {
            errorMessage = 'Authentication service is not available. Please make sure the backend server is running on port 3002.';
          }

          setError(errorMessage);
        }
      }
    } catch (err: any) {
      console.error(`${mode} error:`, err);
      setError(err.message || `An error occurred during ${mode}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 p-6 text-white">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">
              {mode === 'signin' ? 'Sign In' : 'Create Account'}
            </h2>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors duration-200"
              aria-label="Close"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <p className="text-blue-100 mt-1">
            {mode === 'signin'
              ? 'Access your personalized robotics content'
              : 'Join our community to get started'}
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="p-6">
          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="you@example.com"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                placeholder="••••••••"
                required
              />
            </div>

            {mode === 'signup' && (
              <>
                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    placeholder="••••••••"
                    required
                  />
                </div>

                {/* Background questions for signup */}
                <div className="pt-2 border-t border-gray-200">
                  <h3 className="text-sm font-medium text-gray-900 mb-3">Background Information</h3>

                  <div className="mb-4">
                    <label htmlFor="roboticsExperience" className="block text-sm font-medium text-gray-700 mb-1">
                      Your robotics experience
                    </label>
                    <select
                      id="roboticsExperience"
                      value={background.roboticsExperience}
                      onChange={(e) => setBackground({...background, roboticsExperience: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    >
                      <option value="">Select your experience level</option>
                      <option value="none">No experience</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="expert">Expert</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="programmingLanguages" className="block text-sm font-medium text-gray-700 mb-1">
                      Programming languages you know
                    </label>
                    <input
                      type="text"
                      id="programmingLanguages"
                      value={background.programmingLanguages}
                      onChange={(e) => setBackground({...background, programmingLanguages: e.target.value})}
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                      placeholder="e.g., Python, C++, ROS, etc."
                    />
                  </div>
                </div>
              </>
            )}
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full mt-6 py-3 px-4 bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-700 hover:to-indigo-800 text-white font-medium rounded-lg shadow-md transition-all duration-300 transform hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSubmitting ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : mode === 'signin' ? (
              'Sign In'
            ) : (
              'Create Account'
            )}
          </button>
        </form>

        {/* Mode switch */}
        <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
          <p className="text-center text-sm text-gray-600">
            {mode === 'signin' ? "Don't have an account? " : "Already have an account? "}
            <button
              type="button"
              onClick={() => onModeChange(mode === 'signin' ? 'signup' : 'signin')}
              className="font-medium text-blue-600 hover:text-blue-500 transition-colors duration-200"
            >
              {mode === 'signin' ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AuthModal;