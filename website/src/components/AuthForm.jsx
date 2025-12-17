import React, { useState } from 'react';
import { signupUser, loginUser } from '../utils/auth'; // Import from the new auth utility

export default function AuthForm({ onSuccess, onError }) {
  const [formType, setFormType] = useState('login'); // New state for form type
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('');
  const [hardwareBackground, setHardwareBackground] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(''); // New state for error messages

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMessage(''); // Clear previous errors
    try {
      await loginUser(email, password); // Use login utility
      console.log('Login successful');
      localStorage.setItem('loggedInUserEmail', email); // Mock user session
      onSuccess();
    } catch (error) {
      setErrorMessage(error.message || 'Login failed'); // Set error message
      onError(error.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();

    // Client-side validation for required background fields
    if (!softwareBackground.trim()) {
      setErrorMessage('Software background is required');
      onError('Software background is required');
      return;
    }

    if (!hardwareBackground.trim()) {
      setErrorMessage('Hardware background is required');
      onError('Hardware background is required');
      return;
    }

    setLoading(true);
    setErrorMessage(''); // Clear previous errors
    try {
      await signupUser(email, password, { softwareBackground, hardwareBackground }); // Use signup utility
      console.log('Signup successful');
      localStorage.setItem('loggedInUserEmail', email); // Mock user session
      onSuccess();
    } catch (error) {
      setErrorMessage(error.message || 'Signup failed'); // Set error message
      onError(error.message || 'Signup failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="better-auth-container">
      <div className="better-auth-tabs">
        <button
          className={formType === 'login' ? 'active' : ''}
          onClick={() => { setFormType('login'); setErrorMessage(''); }} // Clear error on tab switch
        >
          Login
        </button>
        <button
          className={formType === 'signup' ? 'active' : ''}
          onClick={() => { setFormType('signup'); setErrorMessage(''); }} // Clear error on tab switch
        >
          Sign Up
        </button>
      </div>

      {errorMessage && <p className="error-message">{errorMessage}</p>} {/* Display error message */}

      {formType === 'login' ? (
        <form onSubmit={handleLogin} className="better-auth-form">
          <h2>Login</h2>
          <div>
            <label htmlFor="loginEmail">Email:</label>
            <input
              type="email"
              id="loginEmail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="loginPassword">Password:</label>
            <input
              type="password"
              id="loginPassword"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>
      ) : (
        <form onSubmit={handleSignup} className="better-auth-form">
          <h2>Sign Up</h2>
          <div>
            <label htmlFor="signupEmail">Email:</label>
            <input
              type="email"
              id="signupEmail"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="signupPassword">Password:</label>
            <input
              type="password"
              id="signupPassword"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="softwareBackground">Software Background:</label>
            <input
              type="text"
              id="softwareBackground"
              value={softwareBackground}
              onChange={(e) => setSoftwareBackground(e.target.value)}
              placeholder="e.g., Python, C++, ROS, AI/ML frameworks"
            />
          </div>
          <div>
            <label htmlFor="hardwareBackground">Hardware Background:</label>
            <input
              type="text"
              id="hardwareBackground"
              value={hardwareBackground}
              onChange={(e) => setHardwareBackground(e.target.value)}
              placeholder="e.g., Arduino, Raspberry Pi, NVIDIA Jetson, Robotics platforms"
            />
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Signing up...' : 'Sign Up'}
          </button>
        </form>
      )}
    </div>
  );
}