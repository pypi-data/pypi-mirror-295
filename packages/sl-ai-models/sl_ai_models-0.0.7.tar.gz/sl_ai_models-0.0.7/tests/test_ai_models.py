from sl_ai_models.basic_model_interfaces.ai_model import AiModel
import asyncio
import pytest
from tests.utilities_for_tests import coroutine_testing
from tests.models_to_test import ModelsToTest
from tests.ai_mock_manager import AiModelMockManager
from unittest.mock import Mock
import os
import logging
logger = logging.getLogger(__name__)
from sl_ai_models.perplexity import Perplexity
from sl_ai_models.exa_searcher import ExaSearcher
from sl_ai_models.deepgram_nova2 import DeepgramNova2

@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_response_from_a_direct_call_is_same_ask_mock_value(subclass: type[AiModel]) -> None:
    if subclass in [Perplexity, ExaSearcher, DeepgramNova2]:
        pytest.skip(f"Skipping {subclass.__name__} return value is inconsistent")

    model = subclass()
    model_input = model._get_cheap_input_for_invoke()
    response = asyncio.run(model._mockable_direct_call_to_model(model_input))
    assert response is not None, "Response is None"

    mock_value = model._get_mock_return_for_direct_call_to_model_using_cheap_input()
    logger.info(f"Response: {response}, Mock Value: {mock_value}")

    assert response == mock_value, f"Response is not the same as the mock value. Response: {response}, Mock Value: {mock_value}"


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_ai_model_returns_response_with_invoke(subclass: type[AiModel]) -> None:
    model = subclass()
    model_input = model._get_cheap_input_for_invoke()
    response = asyncio.run(model.invoke(model_input))
    assert response is not None, "Response is None"



@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_ai_model_async_is_not_blocking(subclass: type[AiModel]) -> None:
    # NOTE: Don't mock this unless costs get bad since blocking could be caused at any code level below the mock
    number_of_coroutines_to_run = 5
    list_should_run_under_x_times_first_coroutine = 3

    model_input = subclass._get_cheap_input_for_invoke()
    first_coroutine = subclass().invoke(model_input)
    list_of_coroutines = [subclass().invoke(model_input) for _ in range(number_of_coroutines_to_run)]
    coroutine_testing.assert_coroutines_run_under_x_times_duration_of_benchmark([first_coroutine], list_of_coroutines, x=list_should_run_under_x_times_first_coroutine, allowed_errors_or_timeouts=5)


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_call_limit_error_not_raise_if_not_in_test_env(mocker: Mock, subclass: type[AiModel]) -> None:
    pytest_current_test = os.environ.get('PYTEST_CURRENT_TEST')
    if pytest_current_test is None:
        raise RuntimeError("PYTEST_CURRENT_TEST is not set")
    try:
        del os.environ['PYTEST_CURRENT_TEST']
        model = subclass()
        max_calls = 1

        model._increment_calls_then_error_if_testing_call_limit_reached(max_calls)
        model._increment_calls_then_error_if_testing_call_limit_reached(max_calls)
        model._increment_calls_then_error_if_testing_call_limit_reached(max_calls)
        os.environ['PYTEST_CURRENT_TEST'] = pytest_current_test
    except Exception as e:
        os.environ['PYTEST_CURRENT_TEST'] = pytest_current_test
        assert False, f"Error: {e}"


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_call_limit_error_raised_so_tests_cant_accidentally_create_insane_costs(subclass: type[AiModel]) -> None:
    model = subclass()
    calls_before = model._num_calls_to_dependent_model.get()
    try:
        model._num_calls_to_dependent_model.set(0)
        max_calls = 1
        model._increment_calls_then_error_if_testing_call_limit_reached(max_calls)

        with pytest.raises(RuntimeError):
            model._increment_calls_then_error_if_testing_call_limit_reached(max_calls)
    finally:
        model._num_calls_to_dependent_model.set(calls_before)

@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_langchain_traces_deactivated_if_in_testing_mode(mocker: Mock, subclass: type[AiModel]) -> None:
    model = subclass()
    model._deactivate_langchain_traces_if_in_testing_mode()
    langchain_api_key = os.environ.get('LANGCHAIN_API_KEY')
    tracing_v2 = os.environ.get('LANGCHAIN_TRACING_V2')
    assert langchain_api_key is None, "Langchain traces were not deactivated"
    assert tracing_v2 is None, "Langchain traces were not deactivated"


@pytest.mark.parametrize(
    "subclass",
    ModelsToTest.BASIC_MODEL_LIST
)
def test_special_functions_called_with_direct_call(mocker: Mock, subclass: type[AiModel]):
    model = subclass()
    mock_limiting_function = AiModelMockManager.mock_function_that_throws_error_if_test_limit_reached(mocker)
    mock_langchain_deactivating_function = AiModelMockManager.mock_function_that_deactivates_langchain_tracing(mocker)
    asyncio.run(model._mockable_direct_call_to_model(model._get_cheap_input_for_invoke()))
    limit_function_num_calls = mock_limiting_function.call_count
    langchain_function_num_calls = mock_langchain_deactivating_function.call_count
    assert limit_function_num_calls == 1, f"Model function was not called n=1 times. It was called {limit_function_num_calls} times"
    assert langchain_function_num_calls == 1, f"Langchain function was not called n=1 times. It was called {langchain_function_num_calls} times"