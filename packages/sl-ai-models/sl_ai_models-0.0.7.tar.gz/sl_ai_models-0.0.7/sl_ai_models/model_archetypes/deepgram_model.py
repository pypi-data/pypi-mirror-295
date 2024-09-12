from typing import Any
from abc import ABC
from deepgram import DeepgramClient, PrerecordedOptions, PrerecordedResponse
import os
from pydantic import BaseModel
from sl_ai_models.basic_model_interfaces.named_model import NamedModel
from sl_ai_models.basic_model_interfaces.time_limited_model import TimeLimitedModel
from sl_ai_models.basic_model_interfaces.request_limited_model import RequestLimitedModel
from sl_ai_models.basic_model_interfaces.retryable_model import RetryableModel
import logging
import aiofiles
logger = logging.getLogger(__name__)


class DeepgramOutput(BaseModel):
    transcript: str
    audio_duration_in_seconds: float
    other_data: dict | None = None


class DeepgramAudioToTextModel(
    NamedModel,
    TimeLimitedModel,
    RequestLimitedModel,
    RetryableModel,
    ABC
    ):

    async def invoke_and_return_just_transcript(self, url: str) -> str:
        output = await self.invoke(url)
        return output.transcript


    async def invoke(self, url_or_absolute_file_path: str) -> DeepgramOutput:
        logger.debug(f"Invoking Deepgram model with url: {url_or_absolute_file_path}")
        result = await self.__invoke_with_retry_request_and_time_limits(url_or_absolute_file_path)
        logger.debug(f"Successfully invoked Deepgram model with url: {url_or_absolute_file_path}")
        return result


    @RetryableModel._retry_according_to_model_allowed_tries
    @RequestLimitedModel._wait_till_request_capacity_available
    @TimeLimitedModel._wrap_in_model_defined_timeout
    async def __invoke_with_retry_request_and_time_limits(self, url_or_absolute_file_path: str) -> DeepgramOutput:
        return await self._mockable_direct_call_to_model(url_or_absolute_file_path)


    async def _mockable_direct_call_to_model(self, url_or_absolute_file_path: str) -> DeepgramOutput:
        self._everything_special_to_call_before_direct_call()
        response: PrerecordedResponse = await self.__call_deepgram_online_model(url_or_absolute_file_path)
        output = self.__turn_deepgram_prerecorded_response_into_output(response)
        return output


    async def __call_deepgram_online_model(self, url_or_absolute_file_path: str) -> PrerecordedResponse:
        deepgram_api_key = os.environ.get("DEEPGRAM_API_KEY")
        assert deepgram_api_key is not None
        deepgram = DeepgramClient(deepgram_api_key)
        options = PrerecordedOptions(
            smart_format=True,
            model=self.MODEL_NAME,
            language="en-US",
            diarize=True,
            filler_words=False,
        )

        listener = deepgram.listen.asyncrest.v("1")
        time_out_time = 300
        if url_or_absolute_file_path.startswith("http"):
            payload = {
                'url': url_or_absolute_file_path
            }
            response = await listener.transcribe_url(payload, options, timeout=time_out_time) # type: ignore
        else:
            async with aiofiles.open(url_or_absolute_file_path, "rb") as file:
                buffer_data = await file.read()
            payload = { 'buffer': buffer_data }
            response = await listener.transcribe_file(payload, options, timeout=time_out_time) # type: ignore

        assert isinstance(response, PrerecordedResponse)
        return response


    def __turn_deepgram_prerecorded_response_into_output(self, response: PrerecordedResponse) -> DeepgramOutput:
        response_json: dict = response.to_dict()
        try:
            transcript = response_json["results"]["channels"][0]["alternatives"][0]["paragraphs"]["transcript"] # type: ignore # Any of these things can be None, but its too messy to assert on all of them
            audio_duration = float(response_json["metadata"]["duration"]) # type: ignore
        except Exception as e:
            raise ValueError(f"Error getting transcript from Deepgram response. Error: {e}. Response: {response_json}")
        output = DeepgramOutput(
            transcript=transcript,
            audio_duration_in_seconds=audio_duration,
            other_data=response_json,
            )
        return output


    @staticmethod
    def _get_mock_return_for_direct_call_to_model_using_cheap_input() -> Any:
        return MOCK_RETURN_FOR_DIRECT_CALL_TO_MODEL


    @staticmethod
    def _get_cheap_input_for_invoke() -> Any:
        return "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"



MOCK_RETURN_FOR_DIRECT_CALL_TO_MODEL = DeepgramOutput(
    transcript="\nSpeaker 0: Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it.",
    audio_duration_in_seconds=17.566313,
    other_data={
        "metadata": {
            "transaction_key": "deprecated",
            "request_id": "33080039-be8e-45b7-a5e0-5fd91cff5cf9",
            "sha256": "5324da68ede209a16ac69a38e8cd29cee4d754434a041166cda3a1f5e0b24566",
            "created": "2024-08-16T22:19:30.446Z",
            "duration": 17.566313,
            "channels": 1,
            "models": [
                "30089e05-99d1-4376-b32e-c263170674af"
            ],
            "model_info": {
                "30089e05-99d1-4376-b32e-c263170674af": {
                    "name": "2-general-nova",
                    "version": "2024-01-09.29447",
                    "arch": "nova-2"
                }
            }
        },
        "results": {
            "channels": [
                {
                    "alternatives": [
                        {
                            "transcript": "Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it.",
                            "confidence": 0.99872786,
                            "words": [
                                {
                                    "word": "yep",
                                    "start": 5.52,
                                    "end": 6.02,
                                    "confidence": 0.9958389,
                                    "punctuated_word": "Yep.",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "i",
                                    "start": 7.04,
                                    "end": 7.2799997,
                                    "confidence": 0.512589,
                                    "punctuated_word": "I",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "said",
                                    "start": 7.2799997,
                                    "end": 7.44,
                                    "confidence": 0.9672884,
                                    "punctuated_word": "said",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "it",
                                    "start": 7.44,
                                    "end": 7.6,
                                    "confidence": 0.9997284,
                                    "punctuated_word": "it",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "before",
                                    "start": 7.6,
                                    "end": 7.9199996,
                                    "confidence": 0.7845876,
                                    "punctuated_word": "before,",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "and",
                                    "start": 7.9199996,
                                    "end": 8.08,
                                    "confidence": 0.9998627,
                                    "punctuated_word": "and",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "I'll", "start": 8.08, "end": 8.32, "confidence": 0.99989426, "punctuated_word": "I'll",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "say",
                                    "start": 8.32,
                                    "end": 8.48,
                                    "confidence": 0.9996518,
                                    "punctuated_word": "say",
                                    "speaker": 0,
                                    "speaker_confidence": 0.9121094
                                },
                                {
                                    "word": "it",
                                    "start": 8.48,
                                    "end": 8.639999,
                                    "confidence": 0.9998282,
                                    "punctuated_word": "it",
                                    "speaker": 0,
                                    "speaker_confidence": 0.92822266
                                },
                                {
                                    "word": "again",
                                    "start": 8.639999,
                                    "end": 9.139999,
                                    "confidence": 0.9737228,
                                    "punctuated_word": "again.",
                                    "speaker": 0,
                                    "speaker_confidence": 0.92822266
                                },
                                {
                                    "word": "life",
                                    "start": 9.991312,
                                    "end": 10.391313,
                                    "confidence": 0.99582124,
                                    "punctuated_word": "Life",
                                    "speaker": 0,
                                    "speaker_confidence": 0.92822266
                                },
                                {
                                    "word": "moves",
                                    "start": 10.391313,
                                    "end": 10.711312,
                                    "confidence": 0.9989655,
                                    "punctuated_word": "moves",
                                    "speaker": 0,
                                    "speaker_confidence": 0.92822266
                                },
                                {
                                    "word": "pretty",
                                    "start": 10.711312,
                                    "end": 11.031313,
                                    "confidence": 0.9996259,
                                    "punctuated_word": "pretty",
                                    "speaker": 0,
                                    "speaker_confidence": 0.92822266
                                },
                                {
                                    "word": "fast",
                                    "start": 11.031313,
                                    "end": 11.531313,
                                    "confidence": 0.99960166,
                                    "punctuated_word": "fast.",
                                    "speaker": 0,
                                    "speaker_confidence": 0.92822266
                                },
                                {
                                    "word": "you",
                                    "start": 12.071312,
                                    "end": 12.231313,
                                    "confidence": 0.950412,
                                    "punctuated_word": "You",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "don't", "start": 12.231313, "end": 12.4713125, "confidence": 0.9998907, "punctuated_word": "don't",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "stop",
                                    "start": 12.4713125,
                                    "end": 12.711312,
                                    "confidence": 0.99980956,
                                    "punctuated_word": "stop",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "and",
                                    "start": 12.711312,
                                    "end": 12.871312,
                                    "confidence": 0.99874026,
                                    "punctuated_word": "and",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "look",
                                    "start": 12.871312,
                                    "end": 13.031313,
                                    "confidence": 0.99971575,
                                    "punctuated_word": "look",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "around",
                                    "start": 13.031313,
                                    "end": 13.351313,
                                    "confidence": 0.99964535,
                                    "punctuated_word": "around",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "once",
                                    "start": 13.351313,
                                    "end": 13.591312,
                                    "confidence": 0.99837434,
                                    "punctuated_word": "once",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "in",
                                    "start": 13.591312,
                                    "end": 13.671312,
                                    "confidence": 0.9986059,
                                    "punctuated_word": "in",
                                    "speaker": 0,
                                    "speaker_confidence": 0.8408203
                                },
                                {
                                    "word": "a",
                                    "start": 13.671312,
                                    "end": 13.831312,
                                    "confidence": 0.9862984,
                                    "punctuated_word": "a",
                                    "speaker": 0,
                                    "speaker_confidence": 0.94873047
                                },
                                {
                                    "word": "while",
                                    "start": 13.831312,
                                    "end": 14.331312,
                                    "confidence": 0.93138945,
                                    "punctuated_word": "while,",
                                    "speaker": 0,
                                    "speaker_confidence": 0.94873047
                                },
                                {
                                    "word": "you",
                                    "start": 14.631312,
                                    "end": 14.791312,
                                    "confidence": 0.9974233,
                                    "punctuated_word": "you",
                                    "speaker": 0,
                                    "speaker_confidence": 0.94873047
                                },
                                {
                                    "word": "could",
                                    "start": 14.791312,
                                    "end": 14.951313,
                                    "confidence": 0.9986802,
                                    "punctuated_word": "could",
                                    "speaker": 0,
                                    "speaker_confidence": 0.94873047
                                },
                                {
                                    "word": "miss",
                                    "start": 14.951313,
                                    "end": 15.191313,
                                    "confidence": 0.99872786,
                                    "punctuated_word": "miss",
                                    "speaker": 0,
                                    "speaker_confidence": 0.94873047
                                },
                                {
                                    "word": "it",
                                    "start": 15.191313,
                                    "end": 15.691313,
                                    "confidence": 0.99549305,
                                    "punctuated_word": "it.",
                                    "speaker": 0,
                                    "speaker_confidence": 0.94873047
                                }
                            ],
                            "paragraphs": {
                                "transcript": "\nSpeaker 0: Yep. I said it before, and I'll say it again. Life moves pretty fast. You don't stop and look around once in a while, you could miss it.",
                                "paragraphs": [
                                    {
                                        "sentences": [
                                            {
                                                "text": "Yep.",
                                                "start": 5.52,
                                                "end": 6.02
                                            },
                                            {
                                                "text": "I said it before, and I'll say it again.", "start": 7.04, "end": 9.139999}, {"text": "Life moves pretty fast.", "start": 9.991312, "end": 11.531313}, {"text": "You don't stop and look around once in a while, you could miss it.",
                                                "start": 12.071312,
                                                "end": 15.691313
                                            }
                                        ],
                                        "start": 5.52,
                                        "end": 15.691313,
                                        "num_words": 28,
                                        "speaker": 0
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
)


