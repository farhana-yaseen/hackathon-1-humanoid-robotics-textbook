"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { betterAuth } = require('better-auth');
const { memoryAdapter } = require('better-auth/adapters/memory');
// Initialize Better Auth with memory adapter
const auth = betterAuth({
    secret: process.env.BETTER_AUTH_SECRET,
    baseURL: process.env.BETTER_AUTH_URL || 'http://localhost:3002',
    database: memoryAdapter(),
    socialProviders: {
        google: {
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        },
    },
    user: {
        data: {
            softwareExperience: {
                type: 'string',
                required: false
            },
            hardwareExperience: {
                type: 'string',
                required: false
            },
            roboticsExperience: {
                type: 'string',
                required: false
            },
            programmingLanguages: {
                type: 'string', // Store as JSON string
                required: false
            },
            hardwarePlatforms: {
                type: 'string', // Store as JSON string
                required: false
            },
            yearsOfExperience: {
                type: 'number',
                required: false
            },
            primaryInterest: {
                type: 'string',
                required: false
            },
            educationLevel: {
                type: 'string',
                required: false
            }
        }
    }
});
const app = express();
// Middleware
app.use(cors());
app.use(express.json());
// Mount Better Auth API routes
app.use('/api/auth', auth.handler);
// Custom endpoint to handle user background information
app.post('/api/user-background', async (req, res) => {
    const { userId, background } = req.body;
    try {
        // Update user with background information
        const updatedUser = await auth.$context.user.updateUser({
            userId: userId,
            data: {
                softwareExperience: background.softwareExperience,
                hardwareExperience: background.hardwareExperience,
                roboticsExperience: background.roboticsExperience,
                programmingLanguages: JSON.stringify(background.programmingLanguages || []),
                hardwarePlatforms: JSON.stringify(background.hardwarePlatforms || []),
                yearsOfExperience: background.yearsOfExperience,
                primaryInterest: background.primaryInterest,
                educationLevel: background.educationLevel,
            }
        });
        res.json({ success: true, user: updatedUser });
    }
    catch (error) {
        console.error('Error updating user background:', error);
        res.status(500).json({ error: error.message });
    }
});
// Endpoint to get user background
app.get('/api/user-background/:userId', async (req, res) => {
    const { userId } = req.params;
    try {
        const user = await auth.$context.user.getUserById({
            userId: userId
        });
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        res.json({
            softwareExperience: user.softwareExperience,
            hardwareExperience: user.hardwareExperience,
            roboticsExperience: user.roboticsExperience,
            programmingLanguages: user.programmingLanguages ? JSON.parse(user.programmingLanguages) : [],
            hardwarePlatforms: user.hardwarePlatforms ? JSON.parse(user.hardwarePlatforms) : [],
            yearsOfExperience: user.yearsOfExperience,
            primaryInterest: user.primaryInterest,
            educationLevel: user.educationLevel,
        });
    }
    catch (error) {
        console.error('Error getting user background:', error);
        res.status(500).json({ error: error.message });
    }
});
// Endpoint to save user background during registration
app.post('/api/signup-background', async (req, res) => {
    const { email, background } = req.body;
    try {
        // First, get the user by email
        const user = await auth.$context.user.getUserByEmail({
            email: email
        });
        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }
        // Update user with background information
        const updatedUser = await auth.$context.user.updateUser({
            userId: user.id,
            data: {
                softwareExperience: background.softwareExperience,
                hardwareExperience: background.hardwareExperience,
                roboticsExperience: background.roboticsExperience,
                programmingLanguages: JSON.stringify(background.programmingLanguages || []),
                hardwarePlatforms: JSON.stringify(background.hardwarePlatforms || []),
                yearsOfExperience: background.yearsOfExperience,
                primaryInterest: background.primaryInterest,
                educationLevel: background.educationLevel,
            }
        });
        res.json({ success: true, user: updatedUser });
    }
    catch (error) {
        console.error('Error saving signup background:', error);
        res.status(500).json({ error: error.message });
    }
});
const PORT = process.env.PORT || 3002;
app.listen(PORT, () => {
    console.log(`Auth service running on port ${PORT}`);
});
