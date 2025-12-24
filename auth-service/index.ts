import { Request, Response } from 'express';
import * as dotenv from 'dotenv';
import express from 'express';
import cors from 'cors';
import { betterAuth } from 'better-auth';

dotenv.config();

// Initialize Better Auth with custom user fields for robotics education
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'a_super_secret_key_that_should_be_changed_in_production',
  baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3002',
  // Custom user fields - using the proper API for Better Auth 1.4.6-beta.3
  user: {
    // Add custom fields to the user model
    additionalFields: {
      softwareExperience: {
        type: "string",
        required: false,
        defaultValue: null
      },
      hardwareExperience: {
        type: "string",
        required: false,
        defaultValue: null
      },
      roboticsExperience: {
        type: "string",
        required: false,
        defaultValue: null
      },
      programmingLanguages: {
        type: "string", // Store as JSON string
        required: false,
        defaultValue: null
      },
      hardwarePlatforms: {
        type: "string", // Store as JSON string
        required: false,
        defaultValue: null
      },
      yearsOfExperience: {
        type: "number",
        required: false,
        defaultValue: 0
      },
      primaryInterest: {
        type: "string",
        required: false,
        defaultValue: null
      },
      educationLevel: {
        type: "string",
        required: false,
        defaultValue: null
      }
    }
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  }
});

const app = express();

// Middleware - fix the CORS usage
app.use(cors());
app.use(express.json());

// Mount Better Auth API routes
app.use('/api/auth', auth.handler);

// Custom endpoint to handle user background information
app.post('/api/user-background', async (req: Request, res: Response) => {
  try {
    // For now, return a placeholder response since the API is complex
    res.status(500).json({ error: "API method not implemented with current Better Auth version" });
  } catch (error: any) {
    console.error('Error in user-background endpoint:', error);
    res.status(500).json({ error: error.message });
  }
});

// Endpoint to get user background
app.get('/api/user-background/:userId', async (req: Request, res: Response) => {
  try {
    // For now, return a placeholder response since the API is complex
    res.status(500).json({ error: "API method not implemented with current Better Auth version" });
  } catch (error: any) {
    console.error('Error in getting user background:', error);
    res.status(500).json({ error: error.message });
  }
});

// Endpoint to save user background during registration
app.post('/api/signup-background', async (req: Request, res: Response) => {
  const { email, background } = req.body;

  try {
    // For now, return a placeholder response since the API is complex
    res.status(500).json({ error: "API method not implemented with current Better Auth version" });
  } catch (error: any) {
    console.error('Error in signup-background endpoint:', error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
  console.log(`Auth service running on port ${PORT}`);
});