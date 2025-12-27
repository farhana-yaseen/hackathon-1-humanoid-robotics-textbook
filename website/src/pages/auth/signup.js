import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { signUp, signIn } from '../../auth/betterAuthClient';

export default function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [step, setStep] = useState(1); // 1: basic info or OAuth, 2: background info
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState('');

  // Background information state
  const [background, setBackground] = useState({
    softwareExperience: '',
    hardwareExperience: '',
    roboticsExperience: '',
    programmingLanguages: [],
    hardwarePlatforms: [],
    yearsOfExperience: 0,
    primaryInterest: '',
    educationLevel: ''
  });

  const [newLanguage, setNewLanguage] = useState('');
  const [newPlatform, setNewPlatform] = useState('');

  const handleAddLanguage = () => {
    if (newLanguage.trim() && !background.programmingLanguages.includes(newLanguage.trim())) {
      setBackground({
        ...background,
        programmingLanguages: [...background.programmingLanguages, newLanguage.trim()]
      });
      setNewLanguage('');
    }
  };

  const handleRemoveLanguage = (lang) => {
    setBackground({
      ...background,
      programmingLanguages: background.programmingLanguages.filter(l => l !== lang)
    });
  };

  const handleAddPlatform = () => {
    if (newPlatform.trim() && !background.hardwarePlatforms.includes(newPlatform.trim())) {
      setBackground({
        ...background,
        hardwarePlatforms: [...background.hardwarePlatforms, newPlatform.trim()]
      });
      setNewPlatform('');
    }
  };

  const handleRemovePlatform = (platform) => {
    setBackground({
      ...background,
      hardwarePlatforms: background.hardwarePlatforms.filter(p => p !== platform)
    });
  };

  const handleOAuthSignUp = async (provider) => {
    setIsSubmitting(true);
    setError('');

    try {
      const response = await signIn.social({
        provider,
        callbackURL: '/auth/signup', // Redirect back to signup to collect background info
      });

      if (response?.error) {
        throw new Error(response.error.message);
      }
    } catch (err) {
      console.error(`OAuth ${provider} signup error:`, err);
      setError(err.message || `An error occurred during ${provider} signup`);
      setIsSubmitting(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setIsSubmitting(true);

    try {
      // First, create the account with Better Auth
      const authResponse = await signUp.email({
        email,
        password,
        name: email.split('@')[0], // Use part of email as name
      });

      if (authResponse?.error) {
        throw new Error(authResponse.error.message);
      }

      // After successful signup, save the background information to our Node.js auth service
      const backgroundResponse = await fetch('http://localhost:3002/api/signup-background', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          background: {
            softwareExperience: background.softwareExperience,
            hardwareExperience: background.hardwareExperience,
            roboticsExperience: background.roboticsExperience,
            programmingLanguages: background.programmingLanguages,
            hardwarePlatforms: background.hardwarePlatforms,
            yearsOfExperience: background.yearsOfExperience,
            primaryInterest: background.primaryInterest,
            educationLevel: background.educationLevel
          }
        }),
      });

      const backgroundData = await backgroundResponse.json();

      if (!backgroundResponse.ok) {
        console.warn('Background info not saved:', backgroundData.error);
        // Don't fail the signup if background info fails to save
      }

      alert('Account created successfully!');
      // Redirect to home page
      window.location.href = '/';
    } catch (error) {
      console.error('Signup error:', error);
      setError(error.message || 'An error occurred during signup');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create your account for personalized robotics content">
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl w-full space-y-8 signup-form-container">
          <div className="signup-form-header">
            <h1 className="signup-form-title">Create Your Account</h1>
            <p className="signup-form-subtitle">
              Join our community to access personalized robotics content
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm" role="alert">
              {error}
            </div>
          )}

          {step === 1 && (
            <div className="space-y-6">
              {/* OAuth Sign-up Options */}
              <div className="space-y-4">
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white text-gray-500">Or sign up with</span>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => handleOAuthSignUp('google')}
                    disabled={isSubmitting}
                    className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    <svg className="w-5 h-5" viewBox="0 0 24 24">
                      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                      <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    <span className="ml-2">Google</span>
                  </button>

                  <button
                    onClick={() => handleOAuthSignUp('github')}
                    disabled={isSubmitting}
                    className="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                      <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/>
                    </svg>
                    <span className="ml-2">GitHub</span>
                  </button>
                </div>
              </div>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">Or with email</span>
                </div>
              </div>

              <form onSubmit={(e) => { e.preventDefault(); setStep(2); }} className="space-y-6">
                <div className="space-y-4">
                  <div>
                    <label htmlFor="email" className="signup-form-input-label">
                      Email
                    </label>
                    <input
                      type="email"
                      id="email"
                      className="signup-form-input"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      required
                      placeholder="you@example.com"
                    />
                  </div>

                  <div>
                    <label htmlFor="password" className="signup-form-input-label">
                      Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="signup-form-input"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      placeholder="••••••••"
                    />
                  </div>

                  <div>
                    <label htmlFor="confirmPassword" className="signup-form-input-label">
                      Confirm Password
                    </label>
                    <input
                      type="password"
                      id="confirmPassword"
                      className="signup-form-input"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                      placeholder="••••••••"
                    />
                  </div>
                </div>

                <div>
                  <button
                    type="submit"
                    className="signup-form-button"
                  >
                    Continue to Background Info
                  </button>
                </div>
              </form>

              <div className="signup-form-link">
                <p>
                  Already have an account?{' '}
                  <a href="/auth/signin">
                    Sign in here
                  </a>
                </p>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <div className="signup-form-steps">
                <div className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className={`signup-form-step-indicator ${step >= 1 ? 'signup-form-step-active' : 'signup-form-step-inactive'}`}>
                      1
                    </div>
                    <span className="signup-form-step-label">Account Info</span>
                  </div>

                  <div className="signup-form-step-connector"></div>

                  <div className="flex items-center">
                    <div className={`signup-form-step-indicator ${step >= 2 ? 'signup-form-step-active' : 'signup-form-step-inactive'}`}>
                      2
                    </div>
                    <span className="signup-form-step-label">Background Info</span>
                  </div>
                </div>
              </div>

              <div className="text-center">
                <h2 className="signup-form-step-2-title">Tell Us About Your Background</h2>
                <p className="signup-form-step-2-subtitle">
                  This helps us personalize the content for you.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="signup-form-input-label">
                      Software Experience Level
                    </label>
                    <select
                      className="signup-form-select"
                      value={background.softwareExperience}
                      onChange={(e) => setBackground({...background, softwareExperience: e.target.value})}
                    >
                      <option value="">Select your level</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="expert">Expert</option>
                    </select>
                  </div>

                  <div>
                    <label className="signup-form-input-label">
                      Hardware Experience Level
                    </label>
                    <select
                      className="signup-form-select"
                      value={background.hardwareExperience}
                      onChange={(e) => setBackground({...background, hardwareExperience: e.target.value})}
                    >
                      <option value="">Select your level</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="expert">Expert</option>
                    </select>
                  </div>

                  <div>
                    <label className="signup-form-input-label">
                      Robotics Experience Level
                    </label>
                    <select
                      className="signup-form-select"
                      value={background.roboticsExperience}
                      onChange={(e) => setBackground({...background, roboticsExperience: e.target.value})}
                    >
                      <option value="">Select your level</option>
                      <option value="none">No experience</option>
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="expert">Expert</option>
                    </select>
                  </div>

                  <div>
                    <label className="signup-form-input-label">
                      Years of Experience
                    </label>
                    <select
                      className="signup-form-select"
                      value={background.yearsOfExperience}
                      onChange={(e) => setBackground({...background, yearsOfExperience: parseInt(e.target.value)})}
                    >
                      <option value={0}>Select years</option>
                      {[...Array(20)].map((_, i) => (
                        <option key={i+1} value={i+1}>{i+1} year{((i+1) !== 1) ? 's' : ''}</option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="signup-form-input-label">
                    Programming Languages (add as many as you know)
                  </label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      placeholder="e.g., Python, C++, etc."
                      value={newLanguage}
                      onChange={(e) => setNewLanguage(e.target.value)}
                      className="signup-form-input flex-1"
                    />
                    <button
                      type="button"
                      className="signup-form-add-button"
                      onClick={handleAddLanguage}
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {background.programmingLanguages.map((lang, index) => (
                      <span
                        key={index}
                        className="signup-form-tag"
                      >
                        {lang}
                        <button
                          type="button"
                          onClick={() => handleRemoveLanguage(lang)}
                          className="signup-form-tag-remove"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="signup-form-input-label">
                    Hardware Platforms (add as many as you've worked with)
                  </label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      placeholder="e.g., Arduino, Raspberry Pi, ROS, etc."
                      value={newPlatform}
                      onChange={(e) => setNewPlatform(e.target.value)}
                      className="signup-form-input flex-1"
                    />
                    <button
                      type="button"
                      className="signup-form-add-button"
                      onClick={handleAddPlatform}
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {background.hardwarePlatforms.map((platform, index) => (
                      <span
                        key={index}
                        className="signup-form-tag"
                      >
                        {platform}
                        <button
                          type="button"
                          onClick={() => handleRemovePlatform(platform)}
                          className="signup-form-tag-remove"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="signup-form-input-label">
                      Primary Interest in Robotics
                    </label>
                    <select
                      className="signup-form-select"
                      value={background.primaryInterest}
                      onChange={(e) => setBackground({...background, primaryInterest: e.target.value})}
                    >
                      <option value="">Select your interest</option>
                      <option value="humanoid_robots">Humanoid Robots</option>
                      <option value="industrial_automation">Industrial Automation</option>
                      <option value="service_robots">Service Robots</option>
                      <option value="research">Research</option>
                      <option value="education">Education</option>
                      <option value="hobby">Hobby/Personal Projects</option>
                    </select>
                  </div>

                  <div>
                    <label className="signup-form-input-label">
                      Education Level
                    </label>
                    <select
                      className="signup-form-select"
                      value={background.educationLevel}
                      onChange={(e) => setBackground({...background, educationLevel: e.target.value})}
                    >
                      <option value="">Select your level</option>
                      <option value="high_school">High School</option>
                      <option value="undergraduate">Undergraduate</option>
                      <option value="graduate">Graduate</option>
                      <option value="phd">PhD</option>
                      <option value="professional">Professional</option>
                      <option value="self_taught">Self-Taught</option>
                    </select>
                  </div>
                </div>

                <div className="flex justify-between pt-4">
                  <button
                    type="button"
                    className="signup-form-back-button"
                    onClick={() => setStep(1)}
                    disabled={isSubmitting}
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    className="signup-form-button"
                    disabled={isSubmitting}
                  >
                    {isSubmitting ? (
                      <span className="flex items-center">
                        <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Creating Account...
                      </span>
                    ) : (
                      'Create Account'
                    )}
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}