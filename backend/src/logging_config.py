"""
Logging configuration for the Humanoid Robotics Textbook Platform.
"""
import logging
import logging.config
import os
from datetime import datetime
from pathlib import Path


def setup_logging():
    """
    Set up comprehensive logging configuration for the application.
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Define log file paths
    app_log_file = logs_dir / "app.log"
    auth_log_file = logs_dir / "auth.log"
    rag_log_file = logs_dir / "rag.log"
    translation_log_file = logs_dir / "translation.log"
    error_log_file = logs_dir / "errors.log"

    # Logging configuration
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d] [PID:%(process)d] %(message)s'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}'
            }
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout'
            },
            'app_file': {
                'level': 'INFO',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(app_log_file),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'auth_file': {
                'level': 'INFO',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(auth_log_file),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'rag_file': {
                'level': 'INFO',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(rag_log_file),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'translation_file': {
                'level': 'INFO',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(translation_log_file),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            },
            'error_file': {
                'level': 'ERROR',
                'formatter': 'detailed',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': str(error_log_file),
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'app_file'],
                'level': 'INFO',
                'propagate': False
            },
            'auth': {
                'handlers': ['auth_file'],
                'level': 'INFO',
                'propagate': False
            },
            'rag': {
                'handlers': ['rag_file'],
                'level': 'INFO',
                'propagate': False
            },
            'translation': {
                'handlers': ['translation_file'],
                'level': 'INFO',
                'propagate': False
            },
            'errors': {
                'handlers': ['error_file', 'default'],
                'level': 'ERROR',
                'propagate': False
            }
        }
    }

    # Apply the logging configuration
    logging.config.dictConfig(logging_config)

    # Set specific log levels based on environment
    if os.getenv('ENVIRONMENT') == 'development':
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('auth').setLevel(logging.DEBUG)
        logging.getLogger('rag').setLevel(logging.DEBUG)
        logging.getLogger('translation').setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def get_logger(name: str):
    """
    Get a logger instance with the specified name.

    Args:
        name: The name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


# Initialize logging when module is imported
setup_logging()


# Example usage functions
def log_user_action(user_id: str, action: str, details: dict = None):
    """
    Log a user action with details.

    Args:
        user_id: The ID of the user performing the action
        action: The action being performed
        details: Additional details about the action
    """
    logger = get_logger('auth')
    details_str = f" - Details: {details}" if details else ""
    logger.info(f"User {user_id} performed action: {action}{details_str}")


def log_rag_query(user_id: str, session_id: str, query: str, response_length: int):
    """
    Log a RAG query with relevant information.

    Args:
        user_id: The ID of the user making the query
        session_id: The session ID
        query: The query text
        response_length: Length of the response
    """
    logger = get_logger('rag')
    logger.info(f"RAG Query - User: {user_id}, Session: {session_id}, Query Length: {len(query)}, Response Length: {response_length}")


def log_translation_request(user_id: str, chapter_id: str, source_language: str, target_language: str, success: bool):
    """
    Log a translation request.

    Args:
        user_id: The ID of the user requesting translation
        chapter_id: The chapter being translated
        source_language: Source language
        target_language: Target language
        success: Whether the translation was successful
    """
    logger = get_logger('translation')
    status = "SUCCESS" if success else "FAILED"
    logger.info(f"Translation {status} - User: {user_id}, Chapter: {chapter_id}, {source_language} -> {target_language}")


def log_error(error: Exception, context: str = ""):
    """
    Log an error with context.

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred
    """
    logger = get_logger('errors')
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)