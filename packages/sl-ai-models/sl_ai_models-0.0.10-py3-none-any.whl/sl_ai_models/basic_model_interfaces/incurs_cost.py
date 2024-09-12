from abc import ABC, abstractmethod
from typing import Any, Callable, Coroutine, TypeVar
import functools
from sl_ai_models.resource_managers.monetary_cost_manager import MonetaryCostManager
T = TypeVar('T')


class IncursCost(ABC):
    """
    Interface indicating a model should track its cost in the monetary cost manager.
    """

    @abstractmethod
    def _estimate_before_plus_after_cost_from_model_input(self, *args, **kwargs) -> float:
        pass


    @abstractmethod
    async def _track_cost_in_manager_using_model_response(self, response_from_direct_call: Any, original_cost_prediction: Any) -> None:
        pass


    @staticmethod
    def _wrap_in_cost_limiting_and_tracking(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        @functools.wraps(func)
        async def wrapper(self: IncursCost, *args, **kwargs) -> T:
            predicted_cost = self._estimate_before_plus_after_cost_from_model_input(*args, **kwargs)
            prediction_reciept = MonetaryCostManager.add_usage_prediction_to_parent_managers(predicted_cost)
            MonetaryCostManager.raise_error_if_limit_would_be_reached()

            direct_call_response = await func(self, *args, **kwargs)

            await self._track_cost_in_manager_using_model_response(direct_call_response, prediction_reciept)
            return direct_call_response
        return wrapper


