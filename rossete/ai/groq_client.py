"""
Groq API client wrapper for Rossete.

Provides async interface to Groq API with retry logic and error handling.
"""

import logging
from typing import AsyncIterator, Optional

from groq import AsyncGroq
from tenacity import (
    AsyncRetrying,
    RetryError,
    exponential,
    stop_after_attempt,
    wait_exponential,
)

from ..constants import GROQ_MAX_RETRIES, GROQ_RETRY_WAIT_SECONDS, GROQ_TIMEOUT
from ..exceptions import GroqAPIError, GroqAuthenticationError, GroqRateLimitError, TimeoutError

logger = logging.getLogger(__name__)


class GroqClient:
    """Async client for interacting with Groq API."""

    def __init__(self, api_key: str, model: str, timeout: int = GROQ_TIMEOUT):
        """
        Initialize Groq client.

        Args:
            api_key: Groq API key
            model: Model name (e.g., "mixtral-8x7b-32768")
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.client = AsyncGroq(api_key=api_key)
        self._token_usage = {"total_input": 0, "total_output": 0}

        logger.info(f"Initialized GroqClient with model: {model}")

    async def generate_content(
        self,
        prompt: str,
        system_msg: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate content using Groq API.

        Args:
            prompt: User prompt
            system_msg: System message to set context
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-2.0)

        Returns:
            Generated content

        Raises:
            GroqAuthenticationError: If API key is invalid
            GroqRateLimitError: If rate limit is exceeded
            GroqAPIError: For other API errors
            TimeoutError: If request times out
        """
        messages = []

        if system_msg:
            messages.append({"role": "system", "content": system_msg})

        messages.append({"role": "user", "content": prompt})

        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(GROQ_MAX_RETRIES),
                wait=wait_exponential(
                    multiplier=GROQ_RETRY_WAIT_SECONDS,
                    min=GROQ_RETRY_WAIT_SECONDS,
                    max=60,
                ),
                reraise=True,
            ):
                with attempt:
                    logger.debug(f"Calling Groq API (attempt {attempt.retry_state.attempt_number})")

                    response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        timeout=self.timeout,
                    )

                    # Track token usage
                    if hasattr(response, "usage"):
                        self._token_usage["total_input"] += response.usage.prompt_tokens
                        self._token_usage["total_output"] += response.usage.completion_tokens
                        logger.debug(
                            f"Tokens used - Input: {response.usage.prompt_tokens}, "
                            f"Output: {response.usage.completion_tokens}"
                        )

                    content = response.choices[0].message.content
                    logger.debug(f"Generated {len(content)} characters")
                    return content

        except RetryError as e:
            logger.error(f"Max retries exceeded: {e}")
            raise GroqAPIError(f"Failed after {GROQ_MAX_RETRIES} attempts: {e}") from e
        except Exception as e:
            error_str = str(e).lower()

            if "authentication" in error_str or "invalid api key" in error_str:
                logger.error("Authentication failed with Groq API")
                raise GroqAuthenticationError("Invalid Groq API key") from e

            if "rate limit" in error_str or "429" in error_str:
                logger.error("Rate limit exceeded")
                raise GroqRateLimitError("Groq API rate limit exceeded") from e

            if "timeout" in error_str or isinstance(e, TimeoutError):
                logger.error("Request timeout")
                raise TimeoutError(f"Groq API request timeout: {e}") from e

            logger.error(f"Groq API error: {e}")
            raise GroqAPIError(f"Groq API error: {e}") from e

    async def stream_content(
        self,
        prompt: str,
        system_msg: Optional[str] = None,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> AsyncIterator[str]:
        """
        Stream content generation from Groq API.

        Args:
            prompt: User prompt
            system_msg: System message to set context
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature (0.0-2.0)

        Yields:
            Text chunks as they arrive

        Raises:
            GroqAuthenticationError: If API key is invalid
            GroqRateLimitError: If rate limit is exceeded
            GroqAPIError: For other API errors
        """
        messages = []

        if system_msg:
            messages.append({"role": "system", "content": system_msg})

        messages.append({"role": "user", "content": prompt})

        try:
            logger.debug("Starting streaming Groq API call")

            with self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True,
                timeout=self.timeout,
            ) as response:
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content

                    if hasattr(chunk, "usage"):
                        self._token_usage["total_input"] += chunk.usage.prompt_tokens
                        self._token_usage["total_output"] += chunk.usage.completion_tokens

            logger.debug("Streaming completed")

        except Exception as e:
            error_str = str(e).lower()

            if "authentication" in error_str or "invalid api key" in error_str:
                logger.error("Authentication failed during streaming")
                raise GroqAuthenticationError("Invalid Groq API key") from e

            if "rate limit" in error_str or "429" in error_str:
                logger.error("Rate limit exceeded during streaming")
                raise GroqRateLimitError("Groq API rate limit exceeded") from e

            logger.error(f"Groq streaming error: {e}")
            raise GroqAPIError(f"Groq streaming error: {e}") from e

    def get_usage_stats(self) -> dict:
        """
        Get token usage statistics.

        Returns:
            dict with total_input and total_output token counts
        """
        return {
            "total_input_tokens": self._token_usage["total_input"],
            "total_output_tokens": self._token_usage["total_output"],
            "total_tokens": self._token_usage["total_input"] + self._token_usage["total_output"],
        }

    def reset_usage_stats(self) -> None:
        """Reset token usage statistics."""
        self._token_usage = {"total_input": 0, "total_output": 0}
        logger.debug("Reset token usage statistics")


# Global client instance
_groq_client: Optional[GroqClient] = None


def get_groq_client(api_key: str, model: str) -> GroqClient:
    """
    Get or create Groq client instance.

    Args:
        api_key: Groq API key
        model: Model name

    Returns:
        GroqClient instance
    """
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient(api_key, model)
    return _groq_client


def reset_groq_client() -> None:
    """Reset Groq client (useful for testing)."""
    global _groq_client
    _groq_client = None
