-- Migration: Update user_profiles table for Better-Auth integration

-- Up
-- The user_profiles table already exists from previous implementation
-- We need to ensure it has the required structure for Better-Auth integration
-- Add any missing columns if needed (none needed based on existing structure)

-- Ensure indexes exist
CREATE INDEX IF NOT EXISTS idx_user_profiles_created_at ON user_profiles(created_at);
CREATE INDEX IF NOT EXISTS idx_user_profiles_updated_at ON user_profiles(updated_at);
CREATE INDEX IF NOT EXISTS idx_user_profiles_years_experience ON user_profiles(years_of_experience);
CREATE INDEX IF NOT EXISTS idx_user_profiles_programming_languages ON user_profiles USING GIN (programming_languages);
CREATE INDEX IF NOT EXISTS idx_user_profiles_hardware_platforms ON user_profiles USING GIN (hardware_platforms);

-- Down (to revert this migration)
/*
-- This migration is idempotent, no specific down migration needed
*/