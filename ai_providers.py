"""
AI provider configurations and factory for NyayAI
"""
from abc import ABC, abstractmethod
import os
from typing import Optional, Dict, Any
from config import MODEL_CONFIG

class AIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the AI provider with configuration"""
        pass
    
    @abstractmethod
    def generate_content(self, prompt: str) -> Optional[str]:
        """Generate content using the AI model"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and properly configured"""
        pass

class GeminiProvider(AIProvider):
    """Google's Gemini AI provider through OpenRouter"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.session = None
        self._initialized = False
        
    def initialize(self) -> bool:
        try:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                "HTTP-Referer": "https://github.com/copilot",  # Required by OpenRouter
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
            
            # Test the connection through OpenRouter
            test_response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "google/gemini-pro-1.5",
                    "messages": [{"role": "user", "content": "Test"}],
                    "temperature": MODEL_CONFIG["temperature"],
                    "max_tokens": 10
                }
            )
            test_response.raise_for_status()
            response_data = test_response.json()
            if response_data.get("choices"):
                self._initialized = True
                return True
            else:
                print(f"Unexpected response format: {response_data}")
        except Exception as e:
            print(f"Gemini initialization error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
        return False
    
    def generate_content(self, prompt: str) -> Optional[str]:
        if not self._initialized:
            return None
        try:
            response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "google/gemini-pro-1.5",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": MODEL_CONFIG["temperature"],
                    "max_tokens": MODEL_CONFIG["max_tokens"],
                    "top_p": MODEL_CONFIG["top_p"],
                }
            )
            response.raise_for_status()
            response_json = response.json()
            if response_json and response_json.get("choices"):
                return response_json["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            print(f"Gemini generation error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
            return None
    
    def is_available(self) -> bool:
        return self._initialized and self.session is not None

class OpenAIProvider(AIProvider):
    """OpenAI API provider through OpenRouter"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.session = None
        self._initialized = False
        
    def initialize(self) -> bool:
        try:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                "HTTP-Referer": "https://github.com/copilot",  # Required by OpenRouter
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
            
            # Test the connection through OpenRouter
            test_response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": "Test"}],
                    "temperature": MODEL_CONFIG["temperature"],
                    "max_tokens": 10
                }
            )
            test_response.raise_for_status()
            response_data = test_response.json()
            if response_data.get("choices"):
                self._initialized = True
                return True
            else:
                print(f"Unexpected response format: {response_data}")
        except Exception as e:
            print(f"OpenAI initialization error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
        return False

    def generate_content(self, prompt: str) -> Optional[str]:
        if not self._initialized:
            return None
        try:
            response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": MODEL_CONFIG["temperature"],
                    "max_tokens": MODEL_CONFIG["max_tokens"],
                    "top_p": MODEL_CONFIG["top_p"],
                }
            )
            response.raise_for_status()
            response_json = response.json()
            if response_json and response_json.get("choices"):
                return response_json["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            print(f"OpenAI generation error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
            return None
    
    def is_available(self) -> bool:
        return self._initialized and self.session is not None

class DeepSeekProvider(AIProvider):
    """DeepSeek API provider through OpenRouter"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.session = None
        self._initialized = False
        
    def initialize(self) -> bool:
        try:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                "HTTP-Referer": "https://github.com/copilot",  # Required by OpenRouter
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
            
            # Test the connection through OpenRouter
            test_response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "deepseek/deepseek-chat-v3.1",
                    "messages": [{"role": "user", "content": "Test"}],
                    "temperature": MODEL_CONFIG["temperature"],
                    "max_tokens": 10
                }
            )
            test_response.raise_for_status()
            response_data = test_response.json()
            if response_data.get("choices"):
                self._initialized = True
                return True
            else:
                print(f"Unexpected response format: {response_data}")
        except Exception as e:
            print(f"DeepSeek initialization error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
        return False
    
    def generate_content(self, prompt: str) -> Optional[str]:
        if not self._initialized:
            return None
        try:
            response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "deepseek/deepseek-chat-v3.1",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "top_p": 0.95,
                    "headers": {
                        "HTTP-Referer": "https://github.com/copilot"
                    }
                }
            )
            response.raise_for_status()
            response_json = response.json()
            if response_json and response_json.get("choices"):
                return response_json["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            print(f"DeepSeek generation error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
            return None
    
    def is_available(self) -> bool:
        return self._initialized and self.session is not None

class NemotronProvider(AIProvider):
    """Nemotron Nano model provider through OpenRouter"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key.strip()
        self.session = None
        self._initialized = False
        
    def initialize(self) -> bool:
        try:
            import requests
            self.session = requests.Session()
            self.session.headers.update({
                "HTTP-Referer": "https://github.com/copilot",  # Required by OpenRouter
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            })
            
            # Test the connection through OpenRouter
            test_response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "nvidia/nemotron-nano-12b-v2-vl:free",
                    "messages": [{"role": "user", "content": "Test"}],
                    "temperature": MODEL_CONFIG["temperature"],
                    "max_tokens": 10
                }
            )
            test_response.raise_for_status()
            response_data = test_response.json()
            if response_data.get("choices"):
                self._initialized = True
                return True
            else:
                print(f"Unexpected response format: {response_data}")
        except Exception as e:
            print(f"Nemotron initialization error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
        return False
    
    def generate_content(self, prompt: str) -> Optional[str]:
        if not self._initialized:
            return None
        try:
            response = self.session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json={
                    "model": "nvidia/nemotron-nano-12b-v2-vl:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "top_p": 0.95,
                    "headers": {
                        "HTTP-Referer": "https://github.com/copilot"
                    }
                }
            )
            response.raise_for_status()
            response_json = response.json()
            if response_json and response_json.get("choices"):
                return response_json["choices"][0]["message"]["content"]
            return None
        except Exception as e:
            print(f"Nemotron generation error: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
            return None
    
    def is_available(self) -> bool:
        return self._initialized and self.session is not None

def create_ai_provider(provider_type: str, api_key: str) -> Optional[AIProvider]:
    """Factory function to create AI provider instances"""
    providers = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "deepseek": DeepSeekProvider,
        "nemotron": NemotronProvider
    }
    
    provider_class = providers.get(provider_type.lower())
    if not provider_class:
        print(f"Unknown provider type: {provider_type}")
        return None
    
    provider = provider_class(api_key)
    if provider.initialize():
        return provider
    return None