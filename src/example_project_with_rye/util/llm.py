import sys
from typing import Iterable

import langchain_openai
import openai.lib.azure
from langchain_core.language_models import LanguageModelInput
from langchain_core.messages import AIMessage, ChatMessage
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam
from pydantic.v1 import SecretStr as pydantic_v1_SecretStr

from example_project_with_rye.util.pretty_print import pretty_print_yaml
from example_project_with_rye.util.settings import load_env_settings, Settings


def get_openai_settings_dict(settings: Settings):
    result = {
        "temperature": settings.llm_temperature,
        "top_p": settings.llm_top_p,
        "seed": settings.llm_seed,
        "presence_penalty": settings.llm_presence_penalty,
        "frequency_penalty": settings.llm_frequency_penalty,
    }
    return {k: v for k, v in result.items() if v is not None}


def create_azure_openai_client(settings: Settings) -> openai.lib.azure.AzureOpenAI:
    return openai.lib.azure.AzureOpenAI(
        api_version=settings.llm_version,
        azure_endpoint=settings.llm_endpoint,
        azure_deployment=settings.llm_deployment_name,
        api_key=settings.llm_api_key.get_secret_value(),
        timeout=settings.llm_request_timeout,
        max_retries=settings.llm_max_retries,
        # default_query=get_openai_settings_dict(settings), # does not work
    )


def create_langchain_azure_openai_client(settings: Settings) -> langchain_openai.AzureChatOpenAI:
    return langchain_openai.AzureChatOpenAI(
        api_version=settings.llm_version,
        azure_endpoint=settings.llm_endpoint,
        azure_deployment=settings.llm_deployment_name,
        api_key=pydantic_v1_SecretStr(settings.llm_api_key.get_secret_value()),
        timeout=settings.llm_request_timeout,
        max_retries=settings.llm_max_retries,
        # default_query=get_openai_settings_dict(settings), # does not work
        # model_kwargs=get_openai_settings_dict(settings), # does not work
    )


def execute_openai_chat_completion(
        client: openai.lib.azure.AzureOpenAI,
        settings: Settings,
        messages: Iterable[ChatCompletionMessageParam],
) -> ChatCompletion:
    response = client.chat.completions.create(
        model=settings.llm_deployment_name,
        messages=messages,
        temperature=settings.llm_temperature,
        top_p=settings.llm_top_p,
        seed=settings.llm_seed,
        presence_penalty=settings.llm_presence_penalty,
        frequency_penalty=settings.llm_frequency_penalty,
        logit_bias=settings.llm_logit_bias,
    )
    assert isinstance(response, ChatCompletion)
    print(response.__class__)
    pretty_print_yaml(response.model_dump())
    print(str(response.choices[0].message.content).replace("\n", "\\n"))
    return response


def execute_langchain_openai_chat_completion(
        client: langchain_openai.AzureChatOpenAI,
        settings: Settings,
        messages: LanguageModelInput
) -> AIMessage:
    response = client.invoke(
        input=messages,
        temperature=settings.llm_temperature,
        top_p=settings.llm_top_p,
        seed=settings.llm_seed,
        presence_penalty=settings.llm_presence_penalty,
        frequency_penalty=settings.llm_frequency_penalty,
        logit_bias=settings.llm_logit_bias,
    )
    assert isinstance(response, AIMessage)
    print(response.__class__)
    pretty_print_yaml(response.__dict__)
    print(str(response.content).replace("\n", "\\n"))
    return response


def ask_a_pirate_about_life():
    settings = load_env_settings()

    execute_openai_chat_completion(
        client=create_azure_openai_client(settings),
        settings=settings.model_copy(
            update={
                "llm_logit_bias": {
                    "81236": 20,
                    "9014": -100,
                    "30276": -100,
                    "14789": -100,
                    "2324": -100,
                }
            }
        ),
        messages=[
            {"role": "system", "content": "Always talk like a pirate."},
            {"role": "user", "content": "What is the purpose of life?"},
        ]
    )

    print("====================")
    for ii in range(2):
        execute_openai_chat_completion(
            client=create_azure_openai_client(settings),
            settings=settings,
            messages=[
                {"role": "system", "content": "Always talk like a pirate."},
                {"role": "user", "content": "What is the purpose of life?"},
            ]
        )
    print("-------------")
    for ii in range(2):
        execute_langchain_openai_chat_completion(
            client=create_langchain_azure_openai_client(settings),
            settings=settings,
            messages=[
                ChatMessage(content="Always talk like a pirate.", role="system"),
                ChatMessage(content="What is the purpose of life?", role="user"),
            ]
        )


if __name__ == '__main__':
    ask_a_pirate_about_life()

    sys.exit(0)
