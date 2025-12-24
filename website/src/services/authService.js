// website/src/services/authService.js
// Service to handle authentication with the backend API

const API_BASE_URL = 'http://localhost:8000/api'; // Backend FastAPI server

// Sign up a new user
export const signup = async (email, password, name, background = {}) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        name,
        background, // Pass background info as part of signup
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Signup failed');
    }

    // Store the token in localStorage
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
      localStorage.setItem('userEmail', data.email);
    }

    return {
      success: true,
      user: {
        id: data.user_id,
        email: data.email,
        name: data.email.split('@')[0], // Use part of email as name
      },
      token: data.access_token,
    };
  } catch (error) {
    console.error('Signup error:', error);
    throw error;
  }
};

// Sign in an existing user
export const signin = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/signin`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Signin failed');
    }

    // Store the token in localStorage
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
      localStorage.setItem('userEmail', data.email);
    }

    return {
      success: true,
      user: {
        id: data.user_id,
        email: data.email,
        name: data.name || data.email.split('@')[0],
      },
      token: data.access_token,
    };
  } catch (error) {
    console.error('Signin error:', error);
    throw error;
  }
};

// Sign out the current user
export const signOut = async () => {
  try {
    // Clear the stored token
    localStorage.removeItem('authToken');
    localStorage.removeItem('userEmail');

    return { success: true };
  } catch (error) {
    console.error('Signout error:', error);
    throw error;
  }
};

// Get current session/user info
export const getCurrentSession = () => {
  const token = localStorage.getItem('authToken');
  const email = localStorage.getItem('userEmail');

  if (token && email) {
    // In a real implementation, you would verify the token with the backend
    // For now, we'll return the stored info
    return {
      user: {
        email: email,
        name: email.split('@')[0],
      },
      status: 'authenticated',
    };
  }

  return {
    user: null,
    status: 'unauthenticated',
  };
};

// Update user background
export const updateUserBackground = async (userId, backgroundData) => {
  try {
    const token = localStorage.getItem('authToken');

    const response = await fetch(`${API_BASE_URL}/auth/user-background`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        user_id: userId,
        ...backgroundData,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Update background failed');
    }

    return {
      success: true,
      message: data.message,
    };
  } catch (error) {
    console.error('Update background error:', error);
    throw error;
  }
};