import asyncio
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def add_provider_columns():
    # Connect to the database
    conn = await asyncpg.connect(os.getenv("NEON_DATABASE_URL"))

    try:
        # Add provider and provider_id columns to user_credentials table
        await conn.execute("""
            ALTER TABLE user_credentials
            ADD COLUMN IF NOT EXISTS provider TEXT DEFAULT 'email',
            ADD COLUMN IF NOT EXISTS provider_id TEXT
        """)

        print("Provider columns added successfully!")

        # Verify the columns exist
        result = await conn.fetch("""
            SELECT column_name, data_type, column_default
            FROM information_schema.columns
            WHERE table_name = 'user_credentials'
            AND column_name IN ('provider', 'provider_id')
        """)

        print("Columns in user_credentials table:")
        for row in result:
            print(f"  {row['column_name']}: {row['data_type']} (default: {row['column_default']})")

    except Exception as e:
        print(f"Error adding provider columns: {e}")
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(add_provider_columns())