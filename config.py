"""
Configuration settings for NyayAI application
"""
import os

# App Configuration
APP_TITLE = "NyayAI - Justice Made Simple"
APP_DESCRIPTION = "AI-powered legal assistant for Indian users"

# AI Model Configuration
MODEL_CONFIG = {
    "temperature": 0.3,  # Lower temperature for more focused responses
    "max_tokens": 300,   # Limit response length
    "top_p": 0.8,       # More focused sampling
    "presence_penalty": 0.1,
    "frequency_penalty": 0.1,
}

# UI Colors and Styling
PRIMARY_COLOR = "#1e1e2e"  # Dark blue-gray
SECONDARY_COLOR = "#2d2d44"  # Slightly lighter blue-gray
ACCENT_COLOR = "#6366f1"  # Indigo accent
ACCENT_COLOR_END = "#818cf8"  # Lighter indigo
TEXT_COLOR = "#e2e8f0"  # Light gray for text on dark backgrounds
BACKGROUND_COLOR = "#13151a"  # Very dark background

# Database Configuration
DATABASE_PATH = "nyayai.db"

# File Upload Configuration
MAX_FILE_SIZE_MB = 10
ALLOWED_FILE_TYPES = ["pdf"]

# Sample responses for offline mode
OFFLINE_RESPONSES = {
    "default": "I'm currently in offline mode. Based on general legal knowledge, I recommend consulting with a qualified lawyer for specific legal advice. However, I can help you understand basic legal concepts and direct you to relevant IPC sections.",
    "ipc": "Here are some relevant IPC sections that might apply to your query. Please consult with a legal professional for specific advice.",
    "document": "Document uploaded successfully. In offline mode, I can provide basic document structure analysis, but for detailed legal review, please consult with a qualified attorney."
}

# UI Messages
WELCOME_MESSAGE = """
🏛️ **Welcome to NyayAI - Justice Made Simple**

Your AI-powered legal assistant for Indian law. Get help with:
- Legal queries and advice
- Document summarization
- IPC sections lookup
- Legal draft templates

*Note: This is an AI assistant and should not replace professional legal advice.*
"""