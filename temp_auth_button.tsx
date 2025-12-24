import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import AuthModal from './AuthModal';

const AuthButton = () => {
  const { user, isAuthenticated, signOut } = useAuth();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalMode, setModalMode] = useState<'signin' | 'signup'>('signin');

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  if (isAuthenticated && user) {
    return (
      <div className="flex items-center space-x-4">
        <div className="hidden md:block text-sm text-gray-700">
          Welcome, {user.name || user.email}
        </div>
        <button
          onClick={handleSignOut}
          className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors duration-200"
        >
          Sign Out
        </button>
      </div>
    );
  }

  return (
    <>
      <button
        onClick={() => {
          setModalMode('signin');
          setIsModalOpen(true);
        }}
        className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors duration-200"
      >
        Sign In
      </button>

      <button
        onClick={() => {
          setModalMode('signup');
          setIsModalOpen(true);
        }}
        className="px-4 py-2 text-sm font-medium text-indigo-700 bg-indigo-100 rounded-lg hover:bg-indigo-200 transition-colors duration-200 ml-2"
      >
        Sign Up
      </button>

      <AuthModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        mode={modalMode}
        onModeChange={(mode) => setModalMode(mode)}
      />
    </>
  );
};

export default AuthButton;