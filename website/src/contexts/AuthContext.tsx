import React, { createContext, useContext, ReactNode, useEffect, useState } from 'react';
import { useSession, signIn, signUp, signOut } from '../auth/betterAuthClient';

interface AuthContextType {
  user: any;
  isAuthenticated: boolean;
  loading: boolean;
  signIn: typeof signIn;
  signUp: typeof signUp;
  signOut: typeof signOut;
  updateUserBackground: (background: any) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const { data: session, isLoading } = useSession();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Set loading to false once session data is loaded
    if (!isLoading) {
      setLoading(false);
    }
  }, [isLoading]);

  // Function to update user background information
  const updateUserBackground = async (background: any) => {
    try {
      const userId = session?.user?.id;
      if (!userId) {
        throw new Error('User not authenticated');
      }

      const response = await fetch('/api/user-background', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId,
          background,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to update user background');
      }

      // Optionally refetch session to update user data
      // This would require a mechanism to refresh the session
    } catch (error) {
      console.error('Error updating user background:', error);
      throw error;
    }
  };

  const contextValue: AuthContextType = {
    user: session?.user,
    isAuthenticated: !!session?.user,
    loading: loading,
    signIn,
    signUp,
    signOut: async () => {
      await signOut();
    },
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