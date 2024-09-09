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
        sync_client = instructor.from_openai(OpenAI(), mode=instructor.Mode.TOOLS)
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
        (pydantic_core._pydantic_core.ValidationError, ),
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
        async_client = instructor.from_openai(AsyncOpenAI(), mode=instructor.Mode.TOOLS)
        #async_client = instructor.patch(AsyncOpenAI(mode=instructor.Mode.TOOLS))
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
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are an AI assistant tasked with planning a trip. Use the ReAct pattern to break down your thinking and actions.",
    #     },
    #     {"role": "user", "content": " Plan a 3-day trip to Paris."},
    # ]
    messages = [{'role': 'system', 'content': '\n# Premise\nYou are a software engineer\nHere is some information about this setting\n<Setting Information>\nYou are working to solve a computer science problem. You will need to submit a solution to the problem, which will be tested against a suite of hidden unit tests.\n</Setting Information>\n<Actions Available>\n<edit_submission>\n<action_context>\nEdit the submission code. Use this when you want to make changes to the current solution.\n</action_context>\n<action_arg_spec>\n{\'first_line\': <class \'int\'>, \'last_line\': <class \'int\'>, \'new_code\': <class \'str\'>}\n</action_arg_spec>\n<action_description>\nEdit the submission code\n</action_description>\n\n</edit_submission>\n<add_submission>\n<action_context>\nAdd the submission code. Use this when you want to start from scratch with a new solution.\n</action_context>\n<action_arg_spec>\n{\'submission\': <class \'str\'>}\n</action_arg_spec>\n<action_description>\nAdd the submission code\n</action_description>\n\n</add_submission>\n<add_unit_test>\n<action_context>\nAdd a unit test. The unit test information you submit must be in the format of a BCBUnitTest: \n\nclass BCBUnitTest(BaseModel):\n    test_description: str\n    input_names: List[str]\n    input_types: List[str]\n    input_values: List[Any]\n    assertion_condition: str\n    assertion_type: Literal["assertTrue", "assertRaises"] = "assertTrue"\n\n\n It will be parsed via BCBUnitTest(**unit_test_dict)\n\n\n\n# Some various notes:\n1. If an input should be of a type defined by a specific package, add the package name/alias to the type. E.g. "np.ndarray" or "pd.DataFrame". You still should fully define the value for the input_value field e.g. "pd.DataFrame({\'a\': [1, 2, 3]})"\n\n2. Unit tests will be compiled from the BCBUnitTest class as follows:\n    A. For AssertTrue type tests, the test will be compiled as follows:\n    ```python\n    def test_case(self):\n        # {{self.test_description}}\n\n        {{defs}}\n        result = {{function_name}}(**{{{{args}}}}})\n        self.{{self.assertion_type}}({{self.assertion_condition}})\n    ```\n    B. For AssertRaises type tests, the test will be compiled as follows:\n\n    ```python\n    def test_case(self):\n        # {{self.test_description}}\n        {{defs}}\n        with self.{{self.assertion_type}}({{self.assertion_condition}}):\n            {{function_name}}(**{{{{args}}}}})\n    ```\n\n    Provide information accordingly.\n\n</action_context>\n<action_arg_spec>\n{\'unit_test_name\': <class \'str\'>, \'unit_test_dict\': typing.Dict}\n</action_arg_spec>\n<action_description>\nAdd a unit test\n</action_description>\n\n</add_unit_test>\n<remove_unit_test>\n<action_context>\nRemove a unit test\n</action_context>\n<action_arg_spec>\n{\'unit_test_name\': <class \'str\'>}\n</action_arg_spec>\n<action_description>\nRemove a unit test\n</action_description>\n\n</remove_unit_test>\n<test_submission>\n<action_context>\nTest the submission\n</action_context>\n<action_arg_spec>\n{}\n</action_arg_spec>\n<action_description>\nTest the submission\n</action_description>\n\n</test_submission>\n<submit_solution>\n<action_context>\nSubmit the solution\n</action_context>\n<action_arg_spec>\n{}\n</action_arg_spec>\n<action_description>\nSubmit the solution\n</action_description>\n\n</submit_solution>\n\n</Actions Available>\nYou\'ll be given your past actions/thoughts, along with recent raw observations from the environment\nThe environment one step in the past is your current environment.\n\n# Objective\nPlease complete the problem by drafting a solution, creating unit tests, improving the solution, and submitting the solution.\n\n# Constraints\nYou will be given a code_prompt_for_answer, which contains imports and the function signature. Your solution must comprise code that can be appended to code_prompt_for_answer and run as a single script.\n'}, {'role': 'user', 'content': '\n# Recent Actions / Thoughts\n\n# Recent Observations\n<1 environment step(s) in the past>{\'action_result\': None, \'environment_state\': {\'question\': \'import re\\nfrom urllib.parse import urlparse\\nfrom bs4 import BeautifulSoup\\nimport requests\\n\\n\\ndef task_func(myString):\\n    """\\n    Extracts a URL from a given string and retrieves the title of the web page from that URL. If no valid URL is found,\\n    or the URL does not result in a successful web page fetch, returns an appropriate error message.\\n\\n    Parameters:\\n    myString (str): The string from which to extract the URL.\\n\\n    Returns:\\n    str: The title of the webpage at the extracted URL if successful, otherwise one of the following error messages:\\n        - "No valid URL found in the provided string."\\n        - "Unable to fetch the content of the URL: {url}"\\n        - "No title tag found in the webpage."\\n\\n    Requirements:\\n    - re\\n    - urllib.parse.urlparse\\n    - bs4.BeautifulSoup\\n    - requests\\n\\n    Example:\\n    >>> task_func(\\\'Check this out: https://www.google.com\\\')\\n    \\\'Google\\\'\\n    >>> task_func(\\\'No URL here\\\')\\n    \\\'No valid URL found in the provided string.\\\'\\n    >>> task_func(\\\'Check this broken link: https://www.thisdoesnotexist12345.com\\\')\\n    \\\'Unable to fetch the content of the URL: https://www.thisdoesnotexist12345.com\\\'\\n    """\\n\', \'code_prompt_for_answer\': \'import re\\nfrom urllib.parse import urlparse\\nfrom bs4 import BeautifulSoup\\nimport requests\\ndef task_func(myString):\\n\', \'unit_tests_you_have_written\': {}, \'current_solution\': \'\'}}</1 environment step(s) in the past>\n\nYour next actions / thought: '}]
    
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
