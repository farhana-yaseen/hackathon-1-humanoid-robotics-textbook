-- Migration to add provider columns to user credentials table for social authentication

-- Add provider and provider_id columns to user_credentials table
ALTER TABLE user_credentials
ADD COLUMN IF NOT EXISTS provider TEXT DEFAULT 'email',
ADD COLUMN IF NOT EXISTS provider_id TEXT;

-- Update the updated_at trigger to handle the new columns properly
DROP TRIGGER IF EXISTS update_user_credentials_updated_at ON user_credentials;
DROP FUNCTION IF EXISTS update_updated_at_column_credentials();

-- Recreate the function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column_credentials()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Recreate the trigger to update the updated_at timestamp
CREATE TRIGGER update_user_credentials_updated_at
    BEFORE UPDATE ON user_credentials
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column_credentials();