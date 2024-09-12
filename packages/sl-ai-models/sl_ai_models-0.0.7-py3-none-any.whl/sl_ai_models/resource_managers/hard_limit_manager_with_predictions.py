from __future__ import annotations
from sl_ai_models.resource_managers.hard_limit_manager import HardLimitManager, HardLimitExceededError
from typing import Final
import logging
logger = logging.getLogger(__name__)

# TODO: Add prediction logging to the HardLimitManagerWithPredictions class (if log_usage_when_called is True)

class UsagePrediction:
    __id_counter: int = 0

    def __init__(self, amount: float) -> None:
        self.amount: Final[float] = amount
        UsagePrediction.__id_counter += 1
        self.id: Final[int] = UsagePrediction.__id_counter


class PredictThenResolveHardLimitManager(HardLimitManager):
    def __init__(self, hard_limit: float, log_usage_when_called: bool = False) -> None:
        super().__init__(hard_limit, log_usage_when_called)
        self.__predictions: list[UsagePrediction] = []


    def __enter__(self) -> PredictThenResolveHardLimitManager:
        super().__enter__()
        return self


    @property
    def actual_plus_predicted_usage(self) -> float:
        predicted_usage = sum(prediction.amount for prediction in self.__predictions)
        return self.current_usage + predicted_usage


    @classmethod
    def add_usage_prediction_to_parent_managers(cls, amount: float) -> UsagePrediction:
        if amount < 0:
            raise ValueError("Amount should be a positive number or zero")
        prediction = UsagePrediction(amount)
        for cost_manager in cls._active_limit_managers.get():
            if isinstance(cost_manager, PredictThenResolveHardLimitManager):
                cost_manager.add_usage_prediction_locally(prediction)
            else:
                raise TypeError("active_limit_managers has a manager of the wrong")
        return prediction


    def add_usage_prediction_locally(self, prediction: UsagePrediction) -> None:
        self.__predictions.append(prediction)


    @classmethod
    def raise_error_if_limit_would_be_reached(cls, amount_to_check_room_for: float = 0) -> None:
        super().raise_error_if_limit_would_be_reached(amount_to_check_room_for)
        if amount_to_check_room_for < 0:
            raise ValueError("Amount should be a positive number or zero")
        for cost_manager in cls._active_limit_managers.get():
            if isinstance(cost_manager, PredictThenResolveHardLimitManager):
                if cost_manager.hard_limit - cost_manager.actual_plus_predicted_usage < amount_to_check_room_for:
                    raise HardLimitExceededError(f"It is predictd that the usage amount {amount_to_check_room_for} would push usage beyond the limit. Predicted usage would be pushed to {cost_manager.actual_plus_predicted_usage + amount_to_check_room_for} exceeding the hard limit of {cost_manager.hard_limit}")
            else:
                raise TypeError("active_limit_managers has a manager of the wrong type")


    @classmethod
    def replace_predicted_usage_with_actual_usage_in_parent_managers(cls, prediction_to_replace: UsagePrediction, actual_usage: float) -> None:
        if actual_usage < 0:
            raise ValueError("Actual usage must be non-negative")
        for cost_manager in cls._active_limit_managers.get():
            if isinstance(cost_manager, PredictThenResolveHardLimitManager):
                cost_manager.replace_predicted_usage_with_actual_locally(prediction_to_replace, actual_usage)
            else:
                raise TypeError("active_limit_managers has a manager of the wrong type")


    def replace_predicted_usage_with_actual_locally(self, prediction_to_replace: UsagePrediction, actual_usage: float) -> None:
        if actual_usage < 0:
            raise ValueError("Actual usage must be non-negative")
        if prediction_to_replace not in self.__predictions:
            raise ValueError("Prediction not found")
        self.__predictions.remove(prediction_to_replace)
        self._current_usage += actual_usage
        if self.current_usage > self.hard_limit:
            logger.warning(f"Improperly predicted actual usage. The Hard limit is exceeded. Current Usage: {self.current_usage}. Hard Limit: {self.hard_limit}")
