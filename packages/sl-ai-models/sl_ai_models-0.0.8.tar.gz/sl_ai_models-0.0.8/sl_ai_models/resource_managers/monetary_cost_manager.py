from __future__ import annotations
from sl_ai_models.resource_managers.hard_limit_manager_with_predictions import PredictThenResolveHardLimitManager
from sl_ai_models.resource_managers.hard_limit_manager_with_predictions import UsagePrediction # For other files to easily import from this file #NOSONAR
from sl_ai_models.resource_managers.hard_limit_manager import HardLimitExceededError # For other files to easily import from this file #NOSONAR


class MonetaryCostManager(PredictThenResolveHardLimitManager):
    """
    This class is a subclass of HardLimitManager that is specifically for monetary costs.
    Assume every cost is in USD
    """

    def __enter__(self) -> MonetaryCostManager:
        super().__enter__()
        return self