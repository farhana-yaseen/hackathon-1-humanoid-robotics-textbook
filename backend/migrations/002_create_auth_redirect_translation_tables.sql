-- Migration to create tables for authentication redirect and translation features

-- Create the user_session_extensions table if it doesn't exist
-- This extends the existing user session to track module access and language preferences
CREATE TABLE IF NOT EXISTS user_session_extensions (
    user_id VARCHAR(255) PRIMARY KEY,
    last_module_id VARCHAR(255),
    language_preference VARCHAR(10) DEFAULT 'en',
    last_access_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    default_module_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Create an index on user_id for faster lookups (though it's the primary key)
CREATE INDEX IF NOT EXISTS idx_user_session_extensions_user_id ON user_session_extensions(user_id);

-- Create an index on last_module_id for faster queries
CREATE INDEX IF NOT EXISTS idx_user_session_extensions_last_module ON user_session_extensions(last_module_id);

-- Create the translation_cache table if it doesn't exist
-- This caches translated content to improve performance and reduce API calls
CREATE TABLE IF NOT EXISTS translation_cache (
    content_hash VARCHAR(255) NOT NULL,
    target_language VARCHAR(10) NOT NULL,
    translated_content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    original_content_length INTEGER,
    PRIMARY KEY (content_hash, target_language)
);

-- Create an index on expires_at for efficient cache cleanup
CREATE INDEX IF NOT EXISTS idx_translation_cache_expires ON translation_cache(expires_at);

-- Create an index on content_hash for faster lookups
CREATE INDEX IF NOT EXISTS idx_translation_cache_content ON translation_cache(content_hash);

-- Create the module_access_log table if it doesn't exist
-- This tracks user access to modules for determining "last accessed module"
CREATE TABLE IF NOT EXISTS module_access_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    module_id VARCHAR(255) NOT NULL,
    access_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255),
    position INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
);

-- Create an index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_module_access_log_user ON module_access_log(user_id);

-- Create an index on module_id for faster queries
CREATE INDEX IF NOT EXISTS idx_module_access_log_module ON module_access_log(module_id);

-- Create an index on access_time for sorting by recency
CREATE INDEX IF NOT EXISTS idx_module_access_log_time ON module_access_log(access_time DESC);

-- Create an index for composite queries (user and module)
CREATE INDEX IF NOT EXISTS idx_module_access_log_user_module ON module_access_log(user_id, module_id);

-- Create a trigger to update the updated_at timestamp for user_session_extensions
CREATE OR REPLACE FUNCTION update_user_session_extensions_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_session_extensions_updated_at
    BEFORE UPDATE ON user_session_extensions
    FOR EACH ROW
    EXECUTE FUNCTION update_user_session_extensions_updated_at_column();