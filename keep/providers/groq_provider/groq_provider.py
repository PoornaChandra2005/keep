import json
import dataclasses
import pydantic
import requests

from keep.contextmanager.contextmanager import ContextManager
from keep.providers.base.base_provider import BaseProvider
from keep.providers.models.provider_config import ProviderConfig


@pydantic.dataclasses.dataclass
class GroqProviderAuthConfig:
    api_key: str = dataclasses.field(
        metadata={
            "required": True,
            "description": "Groq Cloud API Key",
            "sensitive": True,
        },
    )


class GroqProvider(BaseProvider):
    PROVIDER_DISPLAY_NAME = "Groq"
    PROVIDER_CATEGORY = ["AI"]

    def __init__(
        self, context_manager: ContextManager, provider_id: str, config: ProviderConfig
    ):
        super().__init__(context_manager, provider_id, config)

    def validate_config(self):
        self.authentication_config = GroqProviderAuthConfig(
            **self.config.authentication
        )

    def dispose(self):
        pass

    def validate_scopes(self) -> dict[str, bool | str]:
        # Validate API key with a simple request
        headers = {
            "Authorization": f"Bearer {self.authentication_config.api_key}",
            "Content-Type": "application/json",
        }
        try:
            # Simple model list call to verify key
            response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
            response.raise_for_status()
            return {"authenticated": True}
        except Exception as e:
            return {"authenticated": str(e)}

    def _query(
        self,
        prompt: str,
        model: str = "llama3-8b-8192",
        max_tokens: int = 1024,
        temperature: float = 0.7,
        **kwargs,
    ):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.authentication_config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        
        # Merge with other optional parameters if provided
        payload.update(kwargs)

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return {
            "response": content,
            "full_response": data
        }


if __name__ == "__main__":
    import os
    import logging

    logging.basicConfig(level=logging.DEBUG, handlers=[logging.StreamHandler()])
    context_manager = ContextManager(
        tenant_id="singletenant",
        workflow_id="test",
    )

    api_key = os.environ.get("GROQ_API_KEY")

    config = ProviderConfig(
        description="Groq Provider",
        authentication={
            "api_key": api_key,
        },
    )

    provider = GroqProvider(
        context_manager=context_manager,
        provider_id="groq-test",
        config=config,
    )

    print(
        provider.query(
            prompt="Hello, who are you?",
            model="llama3-8b-8192",
        )
    )
