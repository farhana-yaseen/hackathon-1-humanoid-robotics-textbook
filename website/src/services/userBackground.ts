// Service to handle user background information storage
// This will communicate with our Node.js auth service

interface UserBackground {
  softwareExperience?: string;
  hardwareExperience?: string;
  roboticsExperience?: string;
  programmingLanguages?: string[];
  hardwarePlatforms?: string[];
  yearsOfExperience?: number;
  primaryInterest?: string;
  educationLevel?: string;
}

export class UserBackgroundService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = (typeof window !== 'undefined' && (window as any).AUTH_API_URL) || 'http://localhost:3002/api';
  }

  async saveUserBackground(userId: string, background: UserBackground): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseUrl}/user-background`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          userId,
          background
        }),
      });

      return response.ok;
    } catch (error) {
      console.error('Error saving user background:', error);
      return false;
    }
  }

  async getUserBackground(userId: string): Promise<UserBackground | null> {
    try {
      const response = await fetch(`${this.baseUrl}/user-background/${userId}`);

      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      console.error('Error getting user background:', error);
      return null;
    }
  }
}

export const userBackgroundService = new UserBackgroundService();