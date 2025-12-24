import { createAuthClient } from "better-auth/client";
import { createFetch } from "@better-fetch/fetch";

// Initialize the Better Auth client
const authClient = createAuthClient({
  fetch: createFetch(),
  // Update this to match your backend's Better Auth endpoint
  baseURL: "http://localhost:8000/api/auth", // This should match your backend Better Auth setup
});

// Extract methods from the auth client
export const { signIn, signUp, signOut } = authClient;

// Ensure useSession is always a function - provide fallback if not available
export const useSession = (typeof authClient.useSession === 'function')
  ? authClient.useSession
  : () => ({ data: null, status: 'unauthenticated', isLoading: false });

// Define user background interface
export interface UserBackground {
  softwareExperience?: string;
  hardwareExperience?: string;
  roboticsExperience?: string;
  programmingLanguages?: string[];
  hardwarePlatforms?: string[];
  yearsOfExperience?: number;
  primaryInterest?: string;
  educationLevel?: string;
}