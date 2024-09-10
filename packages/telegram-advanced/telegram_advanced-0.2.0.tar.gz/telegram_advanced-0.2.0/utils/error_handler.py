# utils/error_handler.py
import traceback
from .logger import CustomLogger

logger = CustomLogger(__name__)

class TelegramBotError(Exception):
    """Base class for exceptions in this module."""
    pass

class APIError(TelegramBotError):
    """Exception raised for errors in the API."""
    pass

class ValidationError(TelegramBotError):
    """Exception raised for validation errors."""
    pass

def handle_error(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except APIError as e:
            logger.error(f"API Error in {func.__name__}: {str(e)}")
            # You might want to retry the API call or take other actions
        except ValidationError as e:
            logger.warning(f"Validation Error in {func.__name__}: {str(e)}")
            # You might want to return a specific error message to the user
        except Exception as e:
            logger.critical(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
            # You might want to notify administrators or take other actions
    return wrapper