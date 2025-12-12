import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { signUp } from '../../auth/betterAuthClient';

export default function SignUp() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [step, setStep] = useState(1); // 1: basic info, 2: background info
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Background information state
  const [background, setBackground] = useState({
    softwareExperience: '',
    hardwareExperience: '',
    roboticsExperience: '',
    programmingLanguages: [] as string[],
    hardwarePlatforms: [] as string[],
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

  const handleRemoveLanguage = (lang: string) => {
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

  const handleRemovePlatform = (platform: string) => {
    setBackground({
      ...background,
      hardwarePlatforms: background.hardwarePlatforms.filter(p => p !== platform)
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert('Passwords do not match');
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
    } catch (error: any) {
      console.error('Signup error:', error);
      alert(`An error occurred during signup: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create your account for personalized robotics content">
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-2xl w-full space-y-8 bg-white p-8 md:p-10 rounded-2xl shadow-lg">
          <div className="text-center">
            <h1 className="text-3xl font-bold text-gray-900">Create Your Account</h1>
            <p className="mt-2 text-sm text-gray-600">
              Join our community to access personalized robotics content
            </p>
          </div>

          <div className="mb-6">
            <div className="flex items-center justify-between">
              <div className={`flex items-center ${step >= 1 ? 'text-blue-600' : 'text-gray-500'}`}>
                <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
                  1
                </div>
                <span className="ml-2 text-sm font-medium hidden sm:block">Account Info</span>
              </div>

              <div className="flex-1 h-0.5 bg-gray-200 mx-4"></div>

              <div className={`flex items-center ${step >= 2 ? 'text-blue-600' : 'text-gray-500'}`}>
                <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'}`}>
                  2
                </div>
                <span className="ml-2 text-sm font-medium hidden sm:block">Background Info</span>
              </div>
            </div>
          </div>

          {step === 1 && (
            <form onSubmit={(e) => { e.preventDefault(); setStep(2); }} className="space-y-6">
              <div className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                    placeholder="you@example.com"
                  />
                </div>

                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                    Password
                  </label>
                  <input
                    type="password"
                    id="password"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    placeholder="••••••••"
                  />
                </div>

                <div>
                  <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm Password
                  </label>
                  <input
                    type="password"
                    id="confirmPassword"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                  className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors"
                >
                  Continue to Background Info
                </button>
              </div>
            </form>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-xl font-bold text-gray-900">Tell Us About Your Background</h2>
                <p className="mt-1 text-sm text-gray-600">
                  This helps us personalize the content for you.
                </p>
              </div>

              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Software Experience Level
                    </label>
                    <select
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Hardware Experience Level
                    </label>
                    <select
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Robotics Experience Level
                    </label>
                    <select
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Years of Experience
                    </label>
                    <select
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Programming Languages (add as many as you know)
                  </label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      placeholder="e.g., Python, C++, etc."
                      value={newLanguage}
                      onChange={(e) => setNewLanguage(e.target.value)}
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    />
                    <button
                      type="button"
                      className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
                      onClick={handleAddLanguage}
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {background.programmingLanguages.map((lang, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center gap-1 px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                      >
                        {lang}
                        <button
                          type="button"
                          onClick={() => handleRemoveLanguage(lang)}
                          className="text-blue-800 hover:text-blue-900 focus:outline-none"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hardware Platforms (add as many as you've worked with)
                  </label>
                  <div className="flex gap-2 mb-2">
                    <input
                      type="text"
                      placeholder="e.g., Arduino, Raspberry Pi, ROS, etc."
                      value={newPlatform}
                      onChange={(e) => setNewPlatform(e.target.value)}
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
                    />
                    <button
                      type="button"
                      className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
                      onClick={handleAddPlatform}
                    >
                      Add
                    </button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {background.hardwarePlatforms.map((platform, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center gap-1 px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm"
                      >
                        {platform}
                        <button
                          type="button"
                          onClick={() => handleRemovePlatform(platform)}
                          className="text-indigo-800 hover:text-indigo-900 focus:outline-none"
                        >
                          ×
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Primary Interest in Robotics
                    </label>
                    <select
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Education Level
                    </label>
                    <select
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
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
                    className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
                    onClick={() => setStep(1)}
                    disabled={isSubmitting}
                  >
                    Back
                  </button>
                  <button
                    type="submit"
                    className="px-6 py-3 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
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