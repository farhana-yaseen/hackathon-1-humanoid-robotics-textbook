"""
UserService for the Humanoid Robotics Textbook application.
"""
from typing import Optional
from ..models.user import User


class UserService:
    """
    Service class to handle user-related operations including profile management.
    """

    def __init__(self):
        """
        Initialize the UserService.
        In a real implementation, this would connect to a database or API.
        """
        # In a real implementation, this would connect to a database
        # For now, using in-memory storage for demonstration
        self.users = {}

    async def get_user(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            user_id: The UUID string of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        return self.users.get(user_id)

    async def update_user_profile(
        self,
        user_id: str,
        software_background: Optional[str] = None,
        hardware_background: Optional[str] = None,
        preferences: Optional[dict] = None
    ) -> Optional[User]:
        """
        Update user profile information.

        Args:
            user_id: The UUID string of the user to update
            software_background: Updated software background
            hardware_background: Updated hardware background
            preferences: Updated user preferences

        Returns:
            Updated User object if successful, None if user not found
        """
        if user_id not in self.users:
            return None

        user = self.users[user_id]
        if software_background is not None:
            user.software_background = software_background
        if hardware_background is not None:
            user.hardware_background = hardware_background
        if preferences is not None:
            user.preferences = preferences

        # Update the updated_at timestamp
        from datetime import datetime
        user.updated_at = datetime.now()

        return user