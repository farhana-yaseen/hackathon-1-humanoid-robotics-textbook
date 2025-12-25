import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { signIn } from '../../auth/betterAuthClient';

export default function SignIn() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError('');

    try {
      const response = await signIn.email({
        email,
        password,
        callbackURL: '/', // Redirect to home page after successful login
      });

      if (response?.error) {
        throw new Error(response.error.message);
      }

      // Better Auth handles session automatically
      // Redirect to home page after successful login
      window.location.href = '/';
    } catch (err) {
      console.error('Signin error:', err);
      setError(err.message || 'An error occurred during signin');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8 bg-white p-10 rounded-2xl shadow-lg signin-form-container">
          <div className="signin-form-header">
            <h1 className="signin-form-title">Welcome back</h1>
            <p className="signin-form-subtitle">
              Sign in to access your personalized robotics content
            </p>
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm" role="alert">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="mt-8 space-y-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="email" className="signin-form-input-label">
                  Email
                </label>
                <input
                  type="email"
                  id="email"
                  className="signin-form-input"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="you@example.com"
                />
              </div>

              <div>
                <label htmlFor="password" className="signin-form-input-label">
                  Password
                </label>
                <input
                  type="password"
                  id="password"
                  className="signin-form-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div>
              <button
                type="submit"
                className="signin-form-button"
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
                  'Sign In'
                )}
              </button>
            </div>
          </form>

          <div className="signin-form-link">
            <p>
              Don't have an account?{' '}
              <a href="/auth/signup">
                Sign up here
              </a>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}