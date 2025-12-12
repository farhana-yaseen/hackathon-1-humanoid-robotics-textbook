import asyncpg
import os
import json
from typing import Optional, List, Dict, Any

DATABASE_URL = os.getenv("NEON_DATABASE_URL")

async def get_db():
    return await asyncpg.connect(DATABASE_URL)


async def save_query(user_query: str, answer: str):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO query_logs (query, answer)
        VALUES ($1, $2)
    """, user_query, answer)
    await conn.close()


async def create_user_profile(user_id: str, software_experience: Optional[str] = None,
                            hardware_experience: Optional[str] = None,
                            robotics_experience: Optional[str] = None,
                            programming_languages: Optional[List[str]] = None,
                            hardware_platforms: Optional[List[str]] = None,
                            years_of_experience: int = 0,
                            primary_interest: Optional[str] = None,
                            education_level: Optional[str] = None):
    """
    Create a new user profile in the database.

    Args:
        user_id: Unique identifier for the user
        software_experience: User's software experience
        hardware_experience: User's hardware experience
        robotics_experience: User's robotics experience
        programming_languages: List of programming languages the user knows
        hardware_platforms: List of hardware platforms the user is familiar with
        years_of_experience: Years of experience
        primary_interest: User's primary interest in robotics
        education_level: User's education level
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute("""
            INSERT INTO user_profiles
            (user_id, software_experience, hardware_experience, robotics_experience,
             programming_languages, hardware_platforms, years_of_experience,
             primary_interest, education_level)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (user_id) DO UPDATE SET
                software_experience = EXCLUDED.software_experience,
                hardware_experience = EXCLUDED.hardware_experience,
                robotics_experience = EXCLUDED.robotics_experience,
                programming_languages = EXCLUDED.programming_languages,
                hardware_platforms = EXCLUDED.hardware_platforms,
                years_of_experience = EXCLUDED.years_of_experience,
                primary_interest = EXCLUDED.primary_interest,
                education_level = EXCLUDED.education_level,
                updated_at = CURRENT_TIMESTAMP
        """, user_id, software_experience, hardware_experience, robotics_experience,
            json.dumps(programming_languages or []), json.dumps(hardware_platforms or []),
            years_of_experience, primary_interest, education_level)
    finally:
        await conn.close()


async def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve a user profile from the database.

    Args:
        user_id: Unique identifier for the user

    Returns:
        Dictionary containing user profile information or None if not found
    """
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        row = await conn.fetchrow("""
            SELECT user_id, software_experience, hardware_experience, robotics_experience,
                   programming_languages, hardware_platforms, years_of_experience,
                   primary_interest, education_level, created_at, updated_at
            FROM user_profiles
            WHERE user_id = $1
        """, user_id)

        if not row:
            return None

        # Parse JSON fields
        return {
            'user_id': row['user_id'],
            'software_experience': row['software_experience'],
            'hardware_experience': row['hardware_experience'],
            'robotics_experience': row['robotics_experience'],
            'programming_languages': json.loads(row['programming_languages']) if row['programming_languages'] else [],
            'hardware_platforms': json.loads(row['hardware_platforms']) if row['hardware_platforms'] else [],
            'years_of_experience': row['years_of_experience'],
            'primary_interest': row['primary_interest'],
            'education_level': row['education_level'],
            'created_at': row['created_at'],
            'updated_at': row['updated_at']
        }
    finally:
        await conn.close()


async def update_user_profile(user_id: str, **kwargs):
    """
    Update a user profile in the database.

    Args:
        user_id: Unique identifier for the user
        **kwargs: Fields to update
    """
    # Filter out None values and prepare the update query
    updates = []
    values = [user_id]  # First value is always user_id for WHERE clause
    param_index = 2  # Start from $2 since $1 is user_id

    for field, value in kwargs.items():
        if field in ['software_experience', 'hardware_experience', 'robotics_experience',
                     'programming_languages', 'hardware_platforms', 'years_of_experience',
                     'primary_interest', 'education_level']:
            if field in ['programming_languages', 'hardware_platforms'] and value is not None:
                updates.append(f"{field} = ${param_index}")
                values.append(json.dumps(value))
                param_index += 1
            else:
                updates.append(f"{field} = ${param_index}")
                values.append(value)
                param_index += 1

    if not updates:
        return  # Nothing to update

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        query = f"""
            UPDATE user_profiles
            SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = $1
        """
        await conn.execute(query, *values)
    finally:
        await conn.close()
