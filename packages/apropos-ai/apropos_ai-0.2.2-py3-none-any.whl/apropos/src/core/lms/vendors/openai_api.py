import backoff
import openai
import pydantic_core
from openai import AsyncOpenAI, OpenAI
from apropos.src.core.lms.cache_init import cache
from apropos.src.core.lms.vendors.openai_like import OpenAIStandardProvider

import instructor
BACKOFF_TOLERANCE = 100  # 20


class OpenAIAPIProvider(OpenAIStandardProvider):
    def __init__(self, force_structured_output=False):
        self.sync_client = OpenAI()
        self.async_client = AsyncOpenAI()
        self.supports_response_model = True
        #self.force_structured_output = force_structured_output

    @backoff.on_exception(
        backoff.expo,
        (pydantic_core._pydantic_core.ValidationError,),
        max_tries=BACKOFF_TOLERANCE,
        logger=None,
        on_giveup=lambda e: print(e)
        if isinstance(e, pydantic_core._pydantic_core.ValidationError)
        else None,
    )
    def sync_chat_completion_with_response_model(
        self, messages, model, temperature, max_tokens, response_model
    ):
        hit = cache.hit_cache(messages, model, temperature, None)
        if hit:
            return hit
        sync_client = instructor.patch(OpenAI())
        output = sync_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_model=response_model,
        )
        # HOPEFULLY WE CAN USE THIS INSTEAD OF THE ABOVE
        # output = self.sync_client.beta.chat.completions.parse(
        #     model=model,
        #     messages=messages,
        #     temperature=temperature,
        #     max_tokens=max_tokens,
        #     response_format=response_model,
        # )
        cache.add_to_cache(messages, model, temperature, None, output)
        return output

    @backoff.on_exception(
        backoff.expo,
        (pydantic_core._pydantic_core.ValidationError,),
        max_tries=BACKOFF_TOLERANCE,
        logger=None,
        on_giveup=lambda e: print(e)
        if isinstance(e, pydantic_core._pydantic_core.ValidationError)
        else None,
    )
    async def async_chat_completion_with_response_model(
        self, messages, model, temperature, max_tokens, response_model
    ):
        hit = cache.hit_cache(messages, model, temperature, None)
        if hit:
            return hit
        async_client = instructor.patch(AsyncOpenAI())
        output = await async_client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_model=response_model,
        )
        # output = await self.async_client.beta.chat.completions.parse(
        #     model=model,
        #     messages=messages,
        #     temperature=temperature,
        #     max_tokens=max_tokens,
        #     response_format=response_model,
        # )
        cache.add_to_cache(messages, model, temperature, None, output)
        print("Output:", output)
        return output
from pydantic import BaseModel
from typing import Dict, Any, List

class ActionArgument(BaseModel):
    argument_name: str
    argument_value: Any

class ReAct(BaseModel):
    reasoning: str
    action: str
    action_args: List[ActionArgument]#Dict[str, Any]

async def react_example():
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant tasked with planning a trip. Use the ReAct pattern to break down your thinking and actions.",
        },
        {"role": "user", "content": "Plan a 3-day trip to Paris."},
    ]
    
    openai_provider = OpenAIAPIProvider()
    response = await openai_provider.async_chat_completion_with_response_model(
        messages=messages,
        model="gpt-4o-2024-08-06",
        temperature=0.7,
        max_tokens=300,
        response_model=ReAct
    )
    
    print(f"Reasoning: {response.reasoning}")
    print(f"Action: {response.action}")
    print(f"Action Args: {response.action_args}")


if __name__ == "__main__":
    import asyncio

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that can answer questions about the capital of France.",
        },
        {"role": "user", "content": "What is the capital of France?"},
    ]
    response = asyncio.run(
        OpenAIAPIProvider().async_chat_completion(
            messages=messages,
            model="gpt-4o-mini",
            temperature=0.0,
            max_tokens=500,
        )
    )
    print(response)
    asyncio.run(react_example())
