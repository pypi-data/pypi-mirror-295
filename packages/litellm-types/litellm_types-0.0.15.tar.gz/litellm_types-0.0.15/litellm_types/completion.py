from pydantic import BaseModel
from typing import Any, Literal, get_type_hints, Awaitable
from beartype import beartype
from typing import Callable, TypeVar, AsyncIterator
from functools import wraps, update_wrapper
import functools
import httpx
import inspect
import rich
import asyncio
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

#  from litellm import acompletion_with_retries
from litellm import acompletion
from openai import AsyncClient
from rich import print
from .messages import AssistantMessage, AnyMessage, ToolCall, ToolCallDelta


class AssistantStream:
    def __init__(self, async_iterator):
        self._iterator = async_iterator

    def __aiter__(self):
        return self

    async def __anext__(self) -> AssistantMessage:
        # Customize behavior here, e.g., modify elements or handle them differently
        try:
            value = await self._iterator.__anext__()
            result_content = value.choices[0].delta.content  # type:ignore
            raw_tool_calls = value.choices[0].delta.tool_calls
            tool_calls = (
                [
                    ToolCallDelta(id=raw_tool_call.id, function=raw_tool_call.function)
                    for raw_tool_call in raw_tool_calls
                ]
                if (raw_tool_calls and len(raw_tool_calls) > 0)
                else None
            )
            if tool_calls is not None and len(tool_calls) == 0:
                tool_calls = None
            return AssistantMessage(
                result_content if result_content else "", tool_calls=tool_calls
            )
        except StopAsyncIteration:
            raise StopAsyncIteration


# ACompletion = Callable[[list[AnyMessage]], Awaitable[AssistantMessage]]
# AStream = Callable[[list[AnyMessage]], Awaitable[AssistantStream]]


def pydantic_to_openai_tool_schema(
    pydantic_class: type[BaseModel],  # function_name: str, function_description: str
) -> dict:
    """
    Convert a Pydantic class to an OpenAI tool function schema.

    Args:
    pydantic_class (BaseModel): The Pydantic class to convert.
    function_name (str): Name of the function for schema.
    function_description (str): Description of the function.

    Returns:
    dict: A dictionary representing the OpenAI tool function schema.
    """
    tool_name = pydantic_class.__name__
    tool_description = pydantic_class.__doc__ or ""
    # Generate JSON schema from Pydantic model
    schema = pydantic_class.model_json_schema()

    # Convert properties to OpenAI tool format
    # properties = {}
    # for key, value in schema["properties"].items():
    #     prop_dict = {
    #         "type": value.get("type"),
    #         "description": value.get("description") if value.get("description") else "",
    #     }
    #     if "enum" in value:
    #         prop_dict["enum"] = value["enum"]
    #     properties[key] = prop_dict
    # Define the OpenAI tool schema for the function

    def remove_title_key(obj):
        if isinstance(obj, dict):
            if "title" in obj:
                del obj["title"]
            for _, value in obj.items():
                remove_title_key(value)
        elif isinstance(obj, list):
            for item in obj:
                remove_title_key(item)

    remove_title_key(schema)
    if "$defs" in schema:
        defs = schema["$defs"]
        del schema["$defs"]

        openai_schema = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": schema,
                "$defs": defs,
            },
        }
    else:
        openai_schema = {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": schema,
            },
        }

    # print(openai_schema)

    return openai_schema


def replace_pydantic_objects_in_tools(
    tools: list[dict | type[BaseModel]] | None,
) -> list[dict] | None:
    if tools is None:
        return None
    fixed_tools: list[dict] = [
        (
            t
            if not (isinstance(t, type) and issubclass(t, BaseModel))
            else pydantic_to_openai_tool_schema(t)
        )
        for t in tools
    ]
    # print(fixed_tools)
    return fixed_tools


class AsyncCompletion:
    def __init__(
        self,
        model: str,
        # Optional OpenAI params: see https://platform.openai.com/docs/api-reference/chat/create
        timeout: float | str | httpx.Timeout | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        n: int | None = None,
        stop=None,
        max_tokens: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        logit_bias: dict | None = None,
        user: str | None = None,
        # openai v1.0+ new params
        response_format: dict | None = None,
        seed: int | None = None,
        tools: list[dict | type[BaseModel]] | None = None,
        tool_choice: str | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        deployment_id=None,
        extra_headers: dict | None = None,
        # soon to be deprecated params by OpenAI
        functions: list | None = None,
        function_call: str | None = None,
        # set api_base, api_version, api_key
        base_url: str | None = None,
        api_version: str | None = None,
        api_key: str | None = None,
        model_list: list | None = None,  # pass in a list of api_base,keys, etc.
        # Optional liteLLM function params
        **kwargs,
    ):
        parsed_tools = replace_pydantic_objects_in_tools(tools)

        async def wrapper(messages: list[AnyMessage]) -> AssistantMessage:
            messages_dicts = [m.__dict__ for m in messages]
            # print(messages_dicts)
            result = await acompletion(
                model=model,
                messages=messages_dicts,
                # timeout=timeout,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=False,
                stop=stop,
                max_tokens=max_tokens,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                user=user,
                response_format=response_format,
                seed=seed,
                tools=parsed_tools,
                tool_choice=tool_choice,
                logprobs=logprobs,
                top_logprobs=top_logprobs,
                deployment_id=deployment_id,
                extra_headers=extra_headers,
                functions=functions,
                function_call=function_call,
                base_url=base_url,
                api_version=api_version,
                api_key=api_key,
                model_list=model_list,
                **kwargs,
            )
            msg_choice = result.choices[0].message
            content = msg_choice.content  # type:ignore
            if hasattr(msg_choice, "tool_calls"):
                raw_tool_calls = msg_choice.tool_calls
                tool_calls = (
                    [ToolCall(id=t.id, function=t.function) for t in raw_tool_calls]
                    if raw_tool_calls
                    else None
                )
            else:
                tool_calls = None
            return AssistantMessage(content=content, tool_calls=tool_calls)

        self.wrapper = wrapper

    async def __call__(self, messages: list[AnyMessage]) -> AssistantMessage:
        return await self.wrapper(messages)


class AsyncStream:
    def __init__(
        self,
        model: str,
        # Optional OpenAI params: see https://platform.openai.com/docs/api-reference/chat/create
        timeout: float | str | httpx.Timeout | None = None,
        temperature: float | None = None,
        top_p: float | None = None,
        n: int | None = None,
        stop=None,
        max_tokens: int | None = None,
        presence_penalty: float | None = None,
        frequency_penalty: float | None = None,
        logit_bias: dict | None = None,
        user: str | None = None,
        # openai v1.0+ new params
        response_format: dict | None = None,
        seed: int | None = None,
        tools: list[dict | type[BaseModel]] | None = None,
        tool_choice: str | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
        deployment_id=None,
        extra_headers: dict | None = None,
        # soon to be deprecated params by OpenAI
        functions: list | None = None,
        function_call: str | None = None,
        # set api_base, api_version, api_key
        base_url: str | None = None,
        api_version: str | None = None,
        api_key: str | None = None,
        model_list: list | None = None,  # pass in a list of api_base,keys, etc.
        # Optional liteLLM function params
        **kwargs,
    ):
        parsed_tools = replace_pydantic_objects_in_tools(tools)

        @retry(
            stop=stop_after_attempt(3),
            wait=wait_exponential(multiplier=1, min=2, max=10),
            retry=retry_if_exception_type((asyncio.TimeoutError, Exception)),
        )
        async def acompletion_with_timeout(*args, **kwargs):
            try:
                return await asyncio.wait_for(
                    acompletion(*args, **kwargs), timeout=30.0
                )
            except asyncio.TimeoutError:
                print(f"acompletion timed out after 30.0 seconds. Retrying...")
                raise

        async def wrapper(messages: list[AnyMessage]) -> AssistantStream:
            messages_dicts = [m.__dict__ for m in messages]
            try:
                result = await acompletion_with_timeout(
                    model=model,
                    messages=messages_dicts,
                    # ... existing parameters ...
                    **kwargs,
                )
                return AssistantStream(result)
            except Exception as e:
                print(f"All retries failed. Last error: {str(e)}")
                raise

        self.wrapper = wrapper

    async def __call__(self, messages: list[AnyMessage]) -> AssistantStream:
        return await self.wrapper(messages)
