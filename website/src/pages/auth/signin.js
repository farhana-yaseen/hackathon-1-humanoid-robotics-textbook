import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { signIn } from '../../auth/betterAuthClient';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');
    setSuccess('');

    try {
      // Use the Better Auth client to sign in
      const response = await signIn.email({
        email,
        password,
        // Don't redirect immediately, handle it after getting redirect URL
      });

      if (response?.error) {
        throw new Error(response.error.message || 'Signin failed');
      }

      // If response has redirect_url (from our backend), use it; otherwise, fetch it
      let redirectUrl = '/';
      if (response.redirect_url) {
        redirectUrl = response.redirect_url;
      } else {
        // Fetch the redirect URL from our backend after successful authentication
        const redirectResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'}/api/auth/redirect-url?user_id=${response.user_id}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (redirectResponse.ok) {
          const redirectData = await redirectResponse.json();
          redirectUrl = redirectData.redirect_url || '/';
        }
      }

      // Show success message with redirect info
      setSuccess(`Sign in successful! Redirecting to ${redirectUrl}...`);

      // Redirect to the appropriate module page after a short delay to show the success message
      setTimeout(() => {
        window.location.href = redirectUrl;
      }, 1500);
    } catch (err) {
      console.error('Signin error:', err);
      let errorMessage = err.message || 'An error occurred during signin';

      // Provide more helpful error message for common issues
      if (err.message?.includes('Failed to fetch') || err.message?.includes('NetworkError')) {
        errorMessage = 'Authentication service is not available. Please make sure the backend server is running.';
      } else if (err.message?.includes('404') || err.message?.includes('not found')) {
        errorMessage = 'Signin service endpoint not found. Please check if the authentication service is configured correctly.';
      }

      setError(errorMessage);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Function to handle social sign-in
  const handleSocialSignIn = async (provider) => {
    setIsSubmitting(true);
    setError('');
    setSuccess('');

    try {
      // In a real implementation, you would redirect to the OAuth provider
      // For now, we'll simulate by opening a popup or redirecting to a social auth endpoint
      // This would typically use a library like @react-oauth/google for Google or similar for GitHub

      // For demonstration, let's make a direct API call to our backend
      // In real implementation, this would involve OAuth flow
      let socialData;
      if (provider === 'google') {
        // This is a placeholder - in real implementation, you'd use Google's OAuth
        // For now, we'll simulate with a mock response
        alert(`Google sign-in would open. In a real implementation, this would redirect to Google OAuth.`);
        return;
      } else if (provider === 'github') {
        // This is a placeholder - in real implementation, you'd use GitHub's OAuth
        alert(`GitHub sign-in would open. In a real implementation, this would redirect to GitHub OAuth.`);
        return;
      }

      // This is where you would process the social login response
      // For now, let's simulate with a direct backend call (not recommended for production)
      // Instead, the real flow would be: Frontend -> OAuth Provider -> Backend with token
    } catch (err) {
      console.error(`${provider} signin error:`, err);
      setError(err.message || `An error occurred during ${provider} sign in`);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className="signin-page-container">
        <div className="signin-card">
          <div className="signin-header">
            <h1 className="signin-title">Welcome back</h1>
            <p className="signin-subtitle">
              Sign in to access your personalized robotics content
            </p>
          </div>

          {success && (
            <div className="signin-success" role="alert">
              {success}
            </div>
          )}
          {error && (
            <div className="signin-error" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="signin-form-group">
              <label htmlFor="email" className="signin-label">
                Email
              </label>
              <input
                type="email"
                id="email"
                className="signin-input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="you@example.com"
              />
            </div>

            <div className="signin-form-group">
              <label htmlFor="password" className="signin-label">
                Password
              </label>
              <input
                type="password"
                id="password"
                className="signin-input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="••••••••"
              />
            </div>

            <div>
              <button
                type="submit"
                className="signin-button"
                disabled={isSubmitting}
              >
                {isSubmitting ? (
                  <span className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Signing In...
                  </span>
                ) : (
                  'Sign In with Email'
                )}
              </button>
            </div>
          </form>

          {/* Social Sign-In Options */}
          <div className="mt-6">
            <div className="signin-separator">
              <div className="signin-separator-line"></div>
              <div className="signin-separator-text">Or continue with</div>
            </div>

            <div className="signin-social-grid">
              <button
                onClick={() => handleSocialSignIn('google')}
                className="signin-social-button"
                disabled={isSubmitting}
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                  <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                  <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                  <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                </svg>
                <span className="ml-2">Google</span>
              </button>

              <button
                onClick={() => handleSocialSignIn('github')}
                className="signin-social-button"
                disabled={isSubmitting}
              >
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                  <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.602-3.369-1.344-3.369-1.344-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/>
                </svg>
                <span className="ml-2">GitHub</span>
              </button>
            </div>
          </div>

          <div className="signin-link-container">
            <p>
              Don't have an account?{' '}
              <a href="/auth/signup" className="signin-link">
                Sign up here
              </a>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}