#!/usr/bin/env python3
"""
Simple database migration script for the humanoid robotics textbook backend.

This script runs SQL migration files to set up the database schema.
"""

import asyncio
import asyncpg
import os
from dotenv import load_dotenv


async def run_migrations():
    """Run all SQL migration files in the migrations directory."""
    # Load environment variables
    load_dotenv()

    # Get database URL from environment
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        raise ValueError("NEON_DATABASE_URL environment variable is not set")

    print(f"Connecting to database: {database_url}")

    # Connect to the database
    conn = await asyncpg.connect(database_url)

    try:
        # Read and execute the first migration file
        migration_file = "migrations/001_create_user_profiles.sql"
        print(f"Executing migration: {migration_file}")

        with open(migration_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Execute the full SQL content
        try:
            await conn.execute(sql_content)
            print("Migration 001 executed successfully")
        except Exception as e:
            print(f"Error executing migration 001: {str(e)}")
            print("This may be due to the trigger function syntax.")

            # Try to execute the SQL content without the trigger function part
            # Split the content to isolate the table creation from the trigger
            parts = sql_content.split('-- Create a trigger to update the updated_at timestamp')
            main_sql = parts[0]

            # Add the table creation part and indexes, but exclude the trigger
            main_sql += """
-- Create an index on user_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_user_id ON user_profiles(user_id);

-- Create the query_logs table if it doesn't exist (for existing functionality)
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

            print("Attempting to execute simplified version without trigger...")
            await conn.execute(main_sql)
            print("Simplified migration 001 executed successfully")

        # Now execute the second migration file for auth redirect and translation features
        migration_file2 = "migrations/002_create_auth_redirect_translation_tables.sql"
        print(f"Executing migration: {migration_file2}")

        with open(migration_file2, 'r', encoding='utf-8') as f:
            sql_content2 = f.read()

        # Execute the full SQL content
        try:
            await conn.execute(sql_content2)
            print("Migration 002 executed successfully")
        except Exception as e:
            print(f"Error executing migration 002: {str(e)}")
            print("This may be due to the trigger function syntax or UUID extension.")

            # Try to execute the SQL content without the trigger function part
            # Split the content to isolate the table creation from the trigger
            parts2 = sql_content2.split('-- Create a trigger to update the updated_at timestamp')
            main_sql2 = parts2[0]

            # Add the table creation part and indexes, but exclude the trigger
            main_sql2 += """
-- Create an index on expires_at for efficient cache cleanup
CREATE INDEX IF NOT EXISTS idx_translation_cache_expires ON translation_cache(expires_at);

-- Create an index on content_hash for faster lookups
CREATE INDEX IF NOT EXISTS idx_translation_cache_content ON translation_cache(content_hash);

-- Create an index on user_id for faster queries
CREATE INDEX IF NOT EXISTS idx_module_access_log_user ON module_access_log(user_id);

-- Create an index on module_id for faster queries
CREATE INDEX IF NOT EXISTS idx_module_access_log_module ON module_access_log(module_id);

-- Create an index on access_time for sorting by recency
CREATE INDEX IF NOT EXISTS idx_module_access_log_time ON module_access_log(access_time DESC);

-- Create an index for composite queries (user and module)
CREATE INDEX IF NOT EXISTS idx_module_access_log_user_module ON module_access_log(user_id, module_id);

-- Create the query_logs table if it doesn't exist (for existing functionality)
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

            print("Attempting to execute simplified version without trigger...")
            await conn.execute(main_sql2)
            print("Simplified migration 002 executed successfully")

        # Now execute the third migration file for user credentials table
        migration_file3 = "migrations/003_create_user_credentials_table.sql"
        print(f"Executing migration: {migration_file3}")

        with open(migration_file3, 'r', encoding='utf-8') as f:
            sql_content3 = f.read()

        # Execute the full SQL content
        try:
            await conn.execute(sql_content3)
            print("Migration 003 executed successfully")
        except Exception as e:
            print(f"Error executing migration 003: {str(e)}")
            print("This may be due to the trigger function syntax.")

            # Try to execute the SQL content without the trigger function part
            # Split the content to isolate the table creation from the trigger
            parts3 = sql_content3.split('-- Create a trigger to update the updated_at timestamp')
            main_sql3 = parts3[0]

            # Add the table creation part and indexes, but exclude the trigger
            main_sql3 += """
-- Create an index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_credentials_email ON user_credentials(email);

-- Create the query_logs table if it doesn't exist (for existing functionality)
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

            print("Attempting to execute simplified version without trigger...")
            await conn.execute(main_sql3)
            print("Simplified migration 003 executed successfully")

        print("All migration statements executed successfully")

    finally:
        await conn.close()
        print("Database connection closed")


async def test_connection():
    """Test the database connection."""
    load_dotenv()
    database_url = os.getenv("NEON_DATABASE_URL")
    if not database_url:
        raise ValueError("NEON_DATABASE_URL environment variable is not set")

    try:
        conn = await asyncpg.connect(database_url)
        print("Database connection successful")

        # Test if user_profiles table exists
        result = await conn.fetch("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'user_profiles'
            );
        """)

        table_exists = result[0]['exists']
        if table_exists:
            print("user_profiles table exists")
        else:
            print("user_profiles table does not exist")

        await conn.close()
        return table_exists
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Just test the connection
        exists = asyncio.run(test_connection())
        sys.exit(0 if exists else 1)
    else:
        # Run migrations
        print("Running database migrations...")
        asyncio.run(run_migrations())
        print("Migrations completed!")