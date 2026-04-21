#!/usr/bin/env python3
"""
Minimal chat example: send "hello", print the model's text reply.

Set env (or use .env) compatible with DeepSeek's Anthropic API, for example:

  ANTHROPIC_AUTH_TOKEN=...
  ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
  ANTHROPIC_MODEL=DeepSeek-V3.2

Also supports ANTHROPIC_API_KEY and MODEL_ID as fallbacks.
"""

import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)


def main() -> None:
    api_key = os.getenv("ANTHROPIC_AUTH_TOKEN") or os.getenv("ANTHROPIC_API_KEY")
    base_url = os.getenv("ANTHROPIC_BASE_URL")
    model = os.getenv("MODEL_ID")

    kwargs = {"api_key": api_key}
    kwargs["base_url"] = base_url

    client = Anthropic(**kwargs)

    user_text = "hello"
    response = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": user_text}],
    )

    parts = []
    for block in response.content:
        if block.type == "text":
            print(block.text)
        elif block.type == "thinking":
            print(block.thinking)
        elif block.type == "tool_use":
            print(block.tool_use)
        elif block.type == "tool_result":
            print(block.tool_result)
        elif block.type == "tool_error":
            print(block.tool_error)
        elif block.type == "tool_timeout":
            print(block.tool_timeout)
        # print(block.text)
    #     if getattr(block, "type", None) == "text" and getattr(block, "text", None):
    #         parts.append(block.text)

    # answer = "\n".join(parts).strip()
    # print(f"User: {user_text}")
    # print(f"Assistant:\n{answer}")


if __name__ == "__main__":
    main()
