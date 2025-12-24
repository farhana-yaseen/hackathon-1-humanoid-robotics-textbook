import React, { createContext, useContext, useEffect, useState } from 'react';
import { useSession, signIn, signUp, signOut } from '../auth/betterAuthClient';

const AuthContext = createContext(undefined);

export const AuthProvider = ({ children }) => {
  const { data: session, isLoading } = useSession();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Set loading to false once session data is loaded
    if (!isLoading) {
      setLoading(false);
    }
  }, [isLoading]);

  // Function to update user background information
  const updateUserBackground = async (background) => {
    try {
      // In Better Auth implementation, we might need to update the user's profile
      // through the Better Auth API or our own profile endpoint
      const response = await fetch('http://localhost:8000/api/auth/create-profile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: session?.user?.id || '', // Using Better Auth user ID
          ...background,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update user background');
      }
    } catch (error) {
      console.error('Error updating user background:', error);
      throw error;
    }
  };

  const contextValue = {
    user: session?.user,
    isAuthenticated: !!session?.user,
    loading: loading,
    signIn,
    signUp,
    signOut,
    updateUserBackground,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};