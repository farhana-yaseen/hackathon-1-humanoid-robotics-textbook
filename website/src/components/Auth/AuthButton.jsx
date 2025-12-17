import React, { useState, useEffect, useRef } from 'react';
import OnboardingForm from './OnboardingForm';

const AuthButton = () => {
  const [showForm, setShowForm] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoginView, setIsLoginView] = useState(true); // true for login, false for signup
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userEmail, setUserEmail] = useState('');
  const dropdownRef = useRef(null);

  // Check if user is already logged in on component mount
  useEffect(() => {
    const loggedInEmail = localStorage.getItem('loggedInUserEmail');
    if (loggedInEmail) {
      setIsLoggedIn(true);
      setUserEmail(loggedInEmail);
    }
  }, []);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowForm(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      // Simulate login API call
      // In a real implementation, you would call the backend API
      console.log('Login attempt with:', { email, password });

      // For demo purposes, we'll just set the user as logged in
      localStorage.setItem('loggedInUserEmail', email);
      setIsLoggedIn(true);
      setUserEmail(email);
      setShowForm(false);

      // Check if user has completed onboarding
      const hasCompletedOnboarding = localStorage.getItem('onboardingCompleted');
      if (!hasCompletedOnboarding) {
        setShowOnboarding(true);
      }
    } catch (err) {
      console.error('Login error:', err);
      setError(err.message || 'An error occurred during login');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      setIsSubmitting(false);
      return;
    }

    try {
      // Simulate signup API call
      // In a real implementation, you would call the backend API
      console.log('Signup attempt with:', { email, password });

      // For demo purposes, we'll just set the user as logged in
      localStorage.setItem('loggedInUserEmail', email);
      setIsLoggedIn(true);
      setUserEmail(email);
      setShowForm(false);

      // Show onboarding form after successful signup
      setShowOnboarding(true);
    } catch (err) {
      console.error('Signup error:', err);
      setError(err.message || 'An error occurred during signup');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('loggedInUserEmail');
    setIsLoggedIn(false);
    setUserEmail('');
  };

  const handleOnboardingComplete = () => {
    localStorage.setItem('onboardingCompleted', 'true');
    setShowOnboarding(false);
  };

  const toggleView = () => {
    setIsLoginView(!isLoginView);
    setError('');
    setEmail('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="relative inline-block" ref={dropdownRef}>
      {isLoggedIn ? (
        <div className="relative">
          <button
            className="px-4 py-2 bg-gray-100 text-gray-800 border border-gray-300 rounded-lg font-medium transition-all duration-200 flex items-center gap-2 hover:bg-gray-200"
            onClick={() => setShowForm(!showForm)}
          >
            <span className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-xs font-bold">
              {userEmail.charAt(0).toUpperCase()}
            </span>
            <span className="hidden max-w-[100px] overflow-hidden text-ellipsis whitespace-nowrap md:inline">
              {userEmail.split('@')[0]}
            </span>
          </button>

          {showForm && (
            <div className="absolute top-full right-0 w-72 bg-white border border-gray-200 rounded-lg shadow-lg z-50 mt-1 overflow-hidden">
              <div className="flex items-center p-4 border-b border-gray-200">
                <div className="w-12 h-12 rounded-full bg-blue-600 text-white flex items-center justify-center text-lg font-bold">
                  {userEmail.charAt(0).toUpperCase()}
                </div>
                <div className="ml-3">
                  <div className="font-semibold text-gray-800">
                    {userEmail.split('@')[0]}
                  </div>
                  <div className="text-xs text-gray-500">
                    {userEmail}
                  </div>
                </div>
              </div>
              <button
                className="w-full py-3 bg-red-50 text-red-600 border-none cursor-pointer font-medium text-left transition-colors duration-200 hover:bg-red-100"
                onClick={handleLogout}
              >
                Sign Out
              </button>
            </div>
          )}
        </div>
      ) : (
        <div className="relative">
          <button
            className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium transition-all duration-200 flex items-center gap-2 hover:opacity-90"
            onClick={() => setShowForm(!showForm)}
          >
            Sign In
          </button>

          {showForm && (
            <div className="absolute top-full right-0 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50 mt-1 overflow-hidden">
              <div className="p-4 border-b border-gray-200">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Sign In</h3>
                <button
                  className="bg-none border-none text-blue-600 cursor-pointer text-sm text-left p-0 w-full"
                  onClick={toggleView}
                >
                  {isLoginView ? 'Need an account? Sign Up' : 'Already have an account? Sign In'}
                </button>
              </div>

              {error && (
                <div className="p-3 bg-red-50 text-red-600 rounded-lg m-4 text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={isLoginView ? handleLogin : handleSignup} className="p-4">
                <div className="mb-4">
                  <label htmlFor="auth-email" className="block mb-1 font-medium text-gray-700 text-sm">Email</label>
                  <input
                    type="email"
                    id="auth-email"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="mb-4">
                  <label htmlFor="auth-password" className="block mb-1 font-medium text-gray-700 text-sm">Password</label>
                  <input
                    type="password"
                    id="auth-password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>

                {!isLoginView && (
                  <div className="mb-4">
                    <label htmlFor="auth-confirm-password" className="block mb-1 font-medium text-gray-700 text-sm">Confirm Password</label>
                    <input
                      type="password"
                      id="auth-confirm-password"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full py-2.5 bg-blue-600 text-white rounded-lg font-medium text-sm cursor-pointer transition-colors duration-200 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                  disabled={isSubmitting}
                >
                  {isSubmitting ? 'Processing...' : (isLoginView ? 'Sign In' : 'Sign Up')}
                </button>
              </form>

              <div className="p-4 pt-0 border-t border-gray-200 text-center">
                <a href="/auth/forgot-password" className="text-blue-600 text-sm hover:underline">
                  Forgot password?
                </a>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Onboarding form overlay */}
      {showOnboarding && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <OnboardingForm
              userId={userEmail ? `user_${Math.abs(hashCode(userEmail)) % 1000000}` : 'unknown'}
              onComplete={handleOnboardingComplete}
            />
          </div>
        </div>
      )}
    </div>
  );
};

// Simple hash function for generating user IDs
function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return hash;
}

export default AuthButton;