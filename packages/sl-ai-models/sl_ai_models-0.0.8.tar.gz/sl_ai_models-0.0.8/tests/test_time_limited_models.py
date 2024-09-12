from sl_ai_models.basic_model_interfaces.ai_model import AiModel
from sl_ai_models.basic_model_interfaces.time_limited_model import TimeLimitedModel
from sl_ai_models.basic_model_interfaces.retryable_model import RetryableModel
import asyncio
import pytest
from unittest.mock import Mock
from tests.models_to_test import ModelsToTest
from tests.ai_mock_manager import AiModelMockManager
import logging
logger = logging.getLogger(__name__)
import time

TIME_LIMITED_ERROR_MESSAGE = "Model must be TimeLimited"


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.TIME_LIMITED_LIST
)
def test_ai_model_successfully_times_out(mocker: Mock, subclass: type[AiModel]) -> None:
    if not issubclass(subclass, TimeLimitedModel):
        raise ValueError(TIME_LIMITED_ERROR_MESSAGE)

    mock_timeout_time = 10
    original_timeout_time = subclass.TIMEOUT_TIME
    subclass.TIMEOUT_TIME = mock_timeout_time

    AiModelMockManager.mock_ai_model_direct_call_with_long_wait(mocker, subclass)
    if issubclass(subclass, RetryableModel):
        model = subclass(allowed_tries=1)
    else:
        model = subclass()
    model_input = model._get_cheap_input_for_invoke()

    try:
        start_time = time.time()
        with pytest.raises(asyncio.exceptions.TimeoutError):
            asyncio.run(model.invoke(model_input))
        end_time = time.time()
        duration = end_time - start_time
        assert duration >= mock_timeout_time, f"Didn't wait long enough. Duration: {duration}, Timeout: {mock_timeout_time}"
        assert duration < mock_timeout_time + 3, f"Waited too long. Duration: {duration}, Timeout: {mock_timeout_time}"
    finally:
        subclass.TIMEOUT_TIME = original_timeout_time


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.TIME_LIMITED_LIST
)
def test_ai_model_does_not_time_out_when_run_time_less_than_timeout_time(mocker: Mock, subclass: type[AiModel]) -> None:
    if not issubclass(subclass, TimeLimitedModel):
        raise ValueError(TIME_LIMITED_ERROR_MESSAGE)

    AiModelMockManager.mock_ai_model_direct_call_with_predefined_mock_value(mocker, subclass)
    model = subclass()
    min_timeout_time = 3
    if model.TIMEOUT_TIME < min_timeout_time:
        raise ValueError(f"TIMEOUT_TIME must be greater than {min_timeout_time} since the mock function still takes time")
    model_input = model._get_cheap_input_for_invoke()
    response = asyncio.run(model.invoke(model_input))
    assert response is not None
