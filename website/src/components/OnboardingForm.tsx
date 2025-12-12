import React, { useState } from 'react';
import { useSession, signUp } from '../auth/betterAuthClient';
import { userBackgroundService, UserBackground } from '../services/userBackground';

interface OnboardingFormProps {
  userId: string;
  onComplete?: () => void;
}

const OnboardingForm: React.FC<OnboardingFormProps> = ({ userId, onComplete }) => {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Background state
  const [background, setBackground] = useState<UserBackground>({
    softwareExperience: '',
    hardwareExperience: '',
    roboticsExperience: '',
    programmingLanguages: [],
    hardwarePlatforms: [],
    yearsOfExperience: 0,
    primaryInterest: '',
    educationLevel: '',
  });

  const [newLanguage, setNewLanguage] = useState('');
  const [newPlatform, setNewPlatform] = useState('');

  const handleAddLanguage = () => {
    if (newLanguage.trim() && !background.programmingLanguages?.includes(newLanguage.trim())) {
      setBackground({
        ...background,
        programmingLanguages: [...(background.programmingLanguages || []), newLanguage.trim()]
      });
      setNewLanguage('');
    }
  };

  const handleRemoveLanguage = (lang: string) => {
    setBackground({
      ...background,
      programmingLanguages: (background.programmingLanguages || []).filter(l => l !== lang)
    });
  };

  const handleAddPlatform = () => {
    if (newPlatform.trim() && !background.hardwarePlatforms?.includes(newPlatform.trim())) {
      setBackground({
        ...background,
        hardwarePlatforms: [...(background.hardwarePlatforms || []), newPlatform.trim()]
      });
      setNewPlatform('');
    }
  };

  const handleRemovePlatform = (platform: string) => {
    setBackground({
      ...background,
      hardwarePlatforms: (background.hardwarePlatforms || []).filter(p => p !== platform)
    });
  };

  const handleNext = () => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      handleSubmit();
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      // Save user background to the auth service
      const success = await userBackgroundService.saveUserBackground(userId, background);

      if (success) {
        onComplete?.();
      } else {
        setError('Failed to save your profile. Please try again.');
      }
    } catch (err) {
      console.error('Error saving user background:', err);
      setError('An error occurred while saving your profile. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Tell us about your background</h3>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Software Experience
              </label>
              <textarea
                value={background.softwareExperience}
                onChange={(e) => setBackground({...background, softwareExperience: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                placeholder="Describe your software development experience..."
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Hardware Experience
              </label>
              <textarea
                value={background.hardwareExperience}
                onChange={(e) => setBackground({...background, hardwareExperience: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                placeholder="Describe your hardware experience..."
              />
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Robotics Experience
              </label>
              <textarea
                value={background.roboticsExperience}
                onChange={(e) => setBackground({...background, roboticsExperience: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                placeholder="Describe your robotics experience..."
              />
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Programming & Platforms</h3>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Programming Languages
              </label>
              <div className="flex mb-2">
                <input
                  type="text"
                  value={newLanguage}
                  onChange={(e) => setNewLanguage(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Add a programming language..."
                />
                <button
                  type="button"
                  onClick={handleAddLanguage}
                  className="px-4 py-2 bg-blue-600 text-white rounded-r-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {(background.programmingLanguages || []).map((lang, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm"
                  >
                    {lang}
                    <button
                      type="button"
                      onClick={() => handleRemoveLanguage(lang)}
                      className="ml-2 text-blue-600 hover:text-blue-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Hardware Platforms
              </label>
              <div className="flex mb-2">
                <input
                  type="text"
                  value={newPlatform}
                  onChange={(e) => setNewPlatform(e.target.value)}
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-l-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Add a hardware platform..."
                />
                <button
                  type="button"
                  onClick={handleAddPlatform}
                  className="px-4 py-2 bg-blue-600 text-white rounded-r-lg text-sm font-medium hover:bg-blue-700 transition-colors"
                >
                  Add
                </button>
              </div>
              <div className="flex flex-wrap gap-2 mt-2">
                {(background.hardwarePlatforms || []).map((platform, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm"
                  >
                    {platform}
                    <button
                      type="button"
                      onClick={() => handleRemovePlatform(platform)}
                      className="ml-2 text-green-600 hover:text-green-800"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>
        );

      case 3:
        return (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-800 mb-4">Additional Details</h3>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Years of Experience
              </label>
              <select
                value={background.yearsOfExperience}
                onChange={(e) => setBackground({...background, yearsOfExperience: parseInt(e.target.value) || 0})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value={0}>Less than 1 year</option>
                <option value={1}>1 year</option>
                <option value={2}>2 years</option>
                <option value={3}>3 years</option>
                <option value={4}>4 years</option>
                <option value={5}>5+ years</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Education Level
              </label>
              <select
                value={background.educationLevel}
                onChange={(e) => setBackground({...background, educationLevel: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select education level</option>
                <option value="high-school">High School</option>
                <option value="undergraduate">Undergraduate</option>
                <option value="graduate">Graduate</option>
                <option value="postgraduate">Postgraduate</option>
                <option value="professional">Professional</option>
              </select>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Primary Interest in Robotics
              </label>
              <input
                type="text"
                value={background.primaryInterest}
                onChange={(e) => setBackground({...background, primaryInterest: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Humanoid robots, Industrial automation, Research, etc."
              />
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <h2 className="text-2xl font-bold text-gray-800">Welcome! Let's personalize your experience</h2>
          <span className="text-sm text-gray-500">Step {step} of 3</span>
        </div>

        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-blue-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(step / 3) * 100}%` }}
          ></div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {renderStep()}

      <div className="flex justify-between mt-6">
        <button
          type="button"
          onClick={handleBack}
          disabled={step === 1}
          className={`px-4 py-2 rounded-lg font-medium text-sm ${
            step === 1
              ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          Back
        </button>

        <button
          type="button"
          onClick={handleNext}
          disabled={loading}
          className={`px-6 py-2 bg-blue-600 text-white rounded-lg font-medium text-sm hover:bg-blue-700 transition-colors ${
            loading ? 'opacity-75 cursor-not-allowed' : ''
          }`}
        >
          {loading ? 'Saving...' : step === 3 ? 'Complete Profile' : 'Next'}
        </button>
      </div>
    </div>
  );
};

export default OnboardingForm;