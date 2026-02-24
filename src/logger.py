import sys
import os
from loguru import logger

# Remove default handler to avoid duplicate logs
logger.remove()

# Add console handler with beautiful formatting
logger.add(
    sys.stdout, 
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Add file handler for persistent logging
logger.add(
    "logs/pageindex_rag.log", 
    rotation="10 MB", 
    retention="10 days", 
    level="DEBUG", 
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
)

def get_logger(name: str):
    """
    Returns a logger instance bound with the specific module name.
    """
    return logger.bind(name=name)
