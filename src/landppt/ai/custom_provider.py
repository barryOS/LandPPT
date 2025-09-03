"""
Custom API Provider for integrating with your own API endpoints
"""

import asyncio
import json
import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
import aiohttp

from .base import AIProvider, AIMessage, AIResponse, MessageRole

logger = logging.getLogger(__name__)

class CustomAPIProvider(AIProvider):
    """
    Custom API provider for integrating with your own API endpoints
    
    This provider allows you to connect to any API that follows a similar
    request/response format. You can customize the request format and
    response parsing to match your API's requirements.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        # Required configuration
        self.api_url = config.get("api_url")
        self.api_key = config.get("api_key")
        
        # Optional configuration with defaults
        self.api_key_header = config.get("api_key_header", "Authorization")
        self.api_key_prefix = config.get("api_key_prefix", "Bearer")
        self.timeout = config.get("timeout", 60)
        self.max_retries = config.get("max_retries", 3)
        
        # Request format configuration
        self.request_format = config.get("request_format", "openai")  # openai, custom
        self.custom_request_template = config.get("custom_request_template", {})
        
        # Response format configuration
        self.response_format = config.get("response_format", "openai")  # openai, custom
        self.response_content_path = config.get("response_content_path", "choices.0.message.content")
        self.response_model_path = config.get("response_model_path", "model")
        self.response_usage_path = config.get("response_usage_path", "usage")
        
        # Validate required configuration
        if not self.api_url:
            raise ValueError("api_url is required for CustomAPIProvider")
        if not self.api_key:
            raise ValueError("api_key is required for CustomAPIProvider")
    
    def _build_headers(self) -> Dict[str, str]:
        """Build request headers with authentication"""
        headers = {
            "Content-Type": "application/json",
        }
        
        if self.api_key_prefix:
            headers[self.api_key_header] = f"{self.api_key_prefix} {self.api_key}"
        else:
            headers[self.api_key_header] = self.api_key
        
        return headers
    
    def _format_request(self, messages: List[AIMessage], **kwargs) -> Dict[str, Any]:
        """Format request based on configuration"""
        config = self._merge_config(**kwargs)
        
        if self.request_format == "openai":
            # OpenAI-compatible format
            return {
                "model": config.get("model", self.model),
                "messages": [
                    {"role": msg.role.value, "content": msg.content}
                    for msg in messages
                ],
                "max_tokens": config.get("max_tokens", 2000),
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 1.0),
                "stream": False
            }
        elif self.request_format == "custom":
            # Use custom template
            request_data = self.custom_request_template.copy()
            
            # Replace placeholders in template
            request_data = self._replace_placeholders(request_data, {
                "model": config.get("model", self.model),
                "messages": [
                    {"role": msg.role.value, "content": msg.content}
                    for msg in messages
                ],
                "max_tokens": config.get("max_tokens", 2000),
                "temperature": config.get("temperature", 0.7),
                "top_p": config.get("top_p", 1.0),
            })
            
            return request_data
        else:
            raise ValueError(f"Unknown request format: {self.request_format}")
    
    def _replace_placeholders(self, data: Any, values: Dict[str, Any]) -> Any:
        """Recursively replace placeholders in data structure"""
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                result[key] = self._replace_placeholders(value, values)
            return result
        elif isinstance(data, list):
            return [self._replace_placeholders(item, values) for item in data]
        elif isinstance(data, str):
            # Replace placeholders like {{model}}, {{messages}}, etc.
            for key, value in values.items():
                placeholder = f"{{{{{key}}}}}"
                if placeholder in data:
                    if isinstance(value, (dict, list)):
                        # If replacing with complex type, return it directly
                        if data == placeholder:
                            return value
                        # Otherwise convert to string
                        data = data.replace(placeholder, json.dumps(value))
                    else:
                        data = data.replace(placeholder, str(value))
            return data
        else:
            return data
    
    def _extract_from_path(self, data: Dict[str, Any], path: str) -> Any:
        """Extract value from nested dictionary using dot notation path"""
        if not path:
            return data
        
        parts = path.split(".")
        current = data
        
        for part in parts:
            if current is None:
                return None
            
            # Handle array index notation like "choices.0"
            if part.isdigit():
                index = int(part)
                if isinstance(current, list) and index < len(current):
                    current = current[index]
                else:
                    return None
            else:
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    return None
        
        return current
    
    def _parse_response(self, response_data: Dict[str, Any]) -> AIResponse:
        """Parse response based on configuration"""
        if self.response_format == "openai":
            # OpenAI-compatible response
            choice = response_data.get("choices", [{}])[0]
            message = choice.get("message", {})
            
            return AIResponse(
                content=message.get("content", ""),
                model=response_data.get("model", self.model),
                usage=response_data.get("usage", {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }),
                finish_reason=choice.get("finish_reason"),
                metadata={"provider": "custom", "api_url": self.api_url}
            )
        elif self.response_format == "custom":
            # Use custom paths to extract data
            content = self._extract_from_path(response_data, self.response_content_path)
            model = self._extract_from_path(response_data, self.response_model_path)
            usage = self._extract_from_path(response_data, self.response_usage_path)
            
            # Ensure content is a string
            if content is None:
                content = ""
            elif not isinstance(content, str):
                content = str(content)
            
            # Ensure usage is a dictionary with expected fields
            if not isinstance(usage, dict):
                usage = {}
            
            usage_dict = {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            }
            
            return AIResponse(
                content=content,
                model=model or self.model,
                usage=usage_dict,
                metadata={"provider": "custom", "api_url": self.api_url}
            )
        else:
            raise ValueError(f"Unknown response format: {self.response_format}")
    
    async def _make_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make HTTP request to API with retry logic"""
        headers = self._build_headers()
        
        async with aiohttp.ClientSession() as session:
            for attempt in range(self.max_retries):
                try:
                    async with session.post(
                        self.api_url,
                        json=request_data,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout)
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
                
                except aiohttp.ClientError as e:
                    logger.error(f"Request attempt {attempt + 1} failed: {e}")
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    async def chat_completion(self, messages: List[AIMessage], **kwargs) -> AIResponse:
        """Generate chat completion using custom API"""
        try:
            # Format request
            request_data = self._format_request(messages, **kwargs)
            
            # Make API request
            response_data = await self._make_request(request_data)
            
            # Parse response
            return self._parse_response(response_data)
            
        except Exception as e:
            logger.error(f"Custom API error: {e}")
            raise
    
    async def text_completion(self, prompt: str, **kwargs) -> AIResponse:
        """Generate text completion using custom API"""
        messages = [AIMessage(role=MessageRole.USER, content=prompt)]
        return await self.chat_completion(messages, **kwargs)
    
    async def stream_chat_completion(self, messages: List[AIMessage], **kwargs) -> AsyncGenerator[str, None]:
        """Stream chat completion (falls back to non-streaming for custom API)"""
        # Most custom APIs don't support streaming, so we fall back to regular completion
        response = await self.chat_completion(messages, **kwargs)
        yield response.content
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "model": self.model,
            "provider": "custom",
            "api_url": self.api_url,
            "request_format": self.request_format,
            "response_format": self.response_format
        }