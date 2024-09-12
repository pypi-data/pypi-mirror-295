import logging
logger = logging.getLogger(__name__)
import tiktoken
from PIL import Image
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionContentPartImageParam, ChatCompletionContentPartTextParam, ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam
from openai.types.chat.chat_completion_content_part_image_param import ImageURL
from tiktoken import Encoding
from typing import Literal
from pydantic import BaseModel
import base64
import math
import re
from io import BytesIO
from urllib import request




class VisionMessageData(BaseModel):
    prompt: str
    b64_image: str
    image_resolution: Literal["auto", "low", "high"]

    def __str__(self) -> str:
        return f"Prompt: {self.prompt}, Resolution: {self.image_resolution}, Image: {self.b64_image[:10]}..."


SMALL_BASE64_IMAGE: str = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
CHEAP_VISION_DATA = VisionMessageData(
    prompt="Hi",
    b64_image=SMALL_BASE64_IMAGE,
    image_resolution="low"
)


class OpenAiUtils:

    @staticmethod
    def text_to_tokens_direct(text_to_tokenize: str, model: str) -> int:
        encoding = tiktoken.encoding_for_model(model)
        token_num = len(encoding.encode(text_to_tokenize))
        return token_num


    @staticmethod
    def messages_to_tokens(messages: list[ChatCompletionMessageParam], model: str) -> int:
        """
        This functions takes in a list of messages and returns the number of tokens in the messages for gpt-3.5-turbo
        Here is an OpenAI guide with the example code: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
        See here for other types of tokenization: https://github.com/shobrook/openlimit/blob/master/openlimit/utilities/token_counters.py
        See here for gpt-vision code. This is an unpublished push to the examples: https://github.com/openai/openai-cookbook/pull/881/commits/555f5bb8b6d09d83fcc7a892562f97d7d1f085c7
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            logger.warning("model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        num_tokens = 0
        for message in messages:
            num_tokens += OpenAiUtils.__message_to_tokens(message, model, encoding)
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
        return num_tokens


    @staticmethod
    def __message_to_tokens(message: ChatCompletionMessageParam, model: str, encoding: Encoding) -> int:
        if OpenAiUtils.__determine_if_message_is_an_image_message(message):
            return OpenAiUtils.__turn_image_message_into_tokens(message, model, encoding)
        else:
            return OpenAiUtils.__turn_regular_message_into_tokens(message, model, encoding)


    @staticmethod
    def __determine_if_message_is_an_image_message(message: ChatCompletionMessageParam) -> bool:
        try:
            content = message["content"] # type: ignore
            content_types = [part["type"] for part in content] # type: ignore
            assert "image_url" in content_types
            return True
        except Exception:
            return False


    @staticmethod
    def __turn_regular_message_into_tokens(message: ChatCompletionMessageParam, model: str, encoding: Encoding) -> int:
        if model in {
            "gpt-3.5-turbo-0613",
            "gpt-3.5-turbo-16k-0613",
            "gpt-4-0314",
            "gpt-4-32k-0314",
            "gpt-4-0613",
            "gpt-4-32k-0613",
            }:
            tokens_per_message = 3
            tokens_per_name = 1
        elif model == "gpt-3.5-turbo-0301":
            tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
            tokens_per_name = -1  # if there's a name, the role is omitted
        elif "gpt-3.5-turbo" in model:
            # gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.
            return OpenAiUtils.__turn_regular_message_into_tokens(message,"gpt-3.5-turbo-0613",encoding)
        elif "gpt-4" in model:
            # gpt-4 may update over time. Returning num tokens assuming gpt-4-0613
            return OpenAiUtils.__turn_regular_message_into_tokens(message, "gpt-4-0613", encoding)
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        num_tokens = tokens_per_message
        for key, value in message.items():
            if not isinstance(value, str):
                raise ValueError(f"Value of key {key} is not a string. The value is {value}")
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
        return num_tokens


    @staticmethod
    def __turn_image_message_into_tokens(message: ChatCompletionMessageParam, model: str, encoding: Encoding) -> int:
        if model not in ["gpt-4-vision-preview", "gpt-4o"]:
            raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}")

        num_tokens: int = 0
        for key, value in message.items():
            if isinstance(value, list):
                for item in value:
                    num_tokens += len(encoding.encode(item["type"]))
                    if item["type"] == "text":
                        num_tokens += len(encoding.encode(item["text"]))
                    elif item["type"] == "image_url":
                        num_tokens += OpenAiUtils.__calculate_tokens_of_image(item["image_url"]["url"], item["image_url"]["detail"])
            elif isinstance(value, str):
                num_tokens += len(encoding.encode(value))

        return num_tokens


    @staticmethod
    def __get_image_dimensions(image_url_or_b64: str) -> tuple[int,int]:
        # regex to check if image is a URL or base64 string
        url_regex = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*)' #NOSONAR
        base_64_regex = r'data:image\/\w+;base64,'
        if re.match(url_regex, image_url_or_b64):
            response = request.urlopen(image_url_or_b64)
            image = Image.open(response)
            return image.size
        elif re.match(base_64_regex, image_url_or_b64):
            image_url_or_b64 = re.sub(r'data:image\/\w+;base64,', '', image_url_or_b64)
            image = Image.open(BytesIO(base64.b64decode(image_url_or_b64)))
            return image.size
        else:
            raise ValueError("Image must be a URL or base64 string.")


    @staticmethod
    def __calculate_tokens_of_image(image_url_or_b64: str, detail:str) -> int:
        # Constants
        LOW_DETAIL_COST = 85
        HIGH_DETAIL_COST_PER_TILE = 170
        ADDITIONAL_COST = 85

        if detail == 'low':
            # Low detail images have a fixed cost
            return LOW_DETAIL_COST
        elif detail == 'high':
            # Calculate token cost for high detail images
            width, height = OpenAiUtils.__get_image_dimensions(image_url_or_b64)
            # Check if resizing is needed to fit within a 2048 x 2048 square
            if max(width, height) > 2048:
                # Resize the image to fit within a 2048 x 2048 square
                ratio = 2048 / max(width, height)
                width = int(width * ratio)
                height = int(height * ratio)

            # Further scale down to 768px on the shortest side
            if min(width, height) > 768:
                ratio = 768 / min(width, height)
                width = int(width * ratio)
                height = int(height * ratio)

            # Calculate the number of 512px squares
            num_squares = math.ceil(width / 512) * math.ceil(height / 512)
            total_cost = num_squares * HIGH_DETAIL_COST_PER_TILE + ADDITIONAL_COST
            return total_cost
        else:
            # Invalid detail_option
            raise ValueError("Invalid detail_option. Use 'low' or 'high'.")


    @staticmethod
    def put_single_user_message_in_list_using_prompt(user_prompt: str) -> list[ChatCompletionMessageParam]:
        return [
            ChatCompletionUserMessageParam(
                role="user",
                content=user_prompt
            )
        ]


    @staticmethod
    def put_single_image_message_in_list_using_gpt_vision_input(vision_data: VisionMessageData) -> list[ChatCompletionMessageParam]:
        prompt: str = vision_data.prompt
        base64_image: str = vision_data.b64_image
        resolution: str = vision_data.image_resolution
        return [
            ChatCompletionUserMessageParam(
                role="user",
                content=[
                    ChatCompletionContentPartTextParam(
                        type="text",
                        text=prompt
                    ),
                    ChatCompletionContentPartImageParam(
                        type="image_url",
                        image_url=ImageURL(
                            url=f"data:image/png;base64,{base64_image}",
                            detail=resolution
                        )
                    )
                ]
            )
        ]


    @staticmethod
    def create_sytem_and_user_message_from_prompt(user_prompt: str, system_prompt: str) -> list[ChatCompletionMessageParam]:
        return [
            ChatCompletionSystemMessageParam(
                role="system",
                content=system_prompt
            ),
            ChatCompletionUserMessageParam(
                role = "user",
                content=user_prompt
            )
        ]


    @classmethod
    def create_system_and_image_message_from_prompt(cls, vision_message_data: VisionMessageData, system_prompt: str) -> list[ChatCompletionMessageParam]:
        image_message_as_list = cls.put_single_image_message_in_list_using_gpt_vision_input(vision_message_data)
        image_message = image_message_as_list[0]
        return [
            ChatCompletionSystemMessageParam(
                role="system",
                content=system_prompt
            ),
            image_message
        ]