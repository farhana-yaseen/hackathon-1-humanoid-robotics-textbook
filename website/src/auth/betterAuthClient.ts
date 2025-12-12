import { createAuthClient } from "better-auth/react";
import { betterFetch } from "@better-fetch/fetch";

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

// Create the auth client
export const authClient = createAuthClient({
  baseURL: typeof window !== 'undefined'
    ? (window as any).ENV?.AUTH_API_URL || "http://localhost:3002"
    : process.env.AUTH_API_URL || "http://localhost:3002",
  fetchConfig: betterFetch,
});

// Destructure the methods
export const { signIn, signUp, signOut, useSession } = authClient;