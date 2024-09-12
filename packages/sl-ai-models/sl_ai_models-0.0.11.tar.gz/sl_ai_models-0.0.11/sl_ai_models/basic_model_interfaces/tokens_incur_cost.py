from sl_ai_models.basic_model_interfaces.incurs_cost import IncursCost
from abc import ABC, abstractmethod
from sl_ai_models.basic_model_interfaces.tokens_are_calculatable import TokensAreCalculatable
from sl_ai_models.resource_managers.monetary_cost_manager import MonetaryCostManager, UsagePrediction
from sl_ai_models.utils.response_types import TextTokenCostResponse
from typing import Any


class TokensIncurCost(TokensAreCalculatable, IncursCost, ABC):

    @abstractmethod
    def caculate_cost_from_tokens(self, prompt_tkns: int, completion_tkns: int) -> float:
        pass


    @abstractmethod
    def input_to_tokens(self, *args, **kwargs) -> int:
        pass


    def _estimate_before_plus_after_cost_from_model_input(self, *args, **kwargs) -> float:
        prompt_tokens = self.input_to_tokens(*args, **kwargs)
        heuristic_multiplier_for_completion_tokens = 2.5
        estimated_completion_tokens = int(prompt_tokens * heuristic_multiplier_for_completion_tokens)
        estimated_cost = self.caculate_cost_from_tokens(prompt_tkns=prompt_tokens, completion_tkns=estimated_completion_tokens)
        return estimated_cost


    async def _track_cost_in_manager_using_model_response(self, response_from_direct_call: Any, original_prediction: UsagePrediction) -> None:
        if isinstance(response_from_direct_call, TextTokenCostResponse):
            cost = response_from_direct_call.cost
        else:
            raise NotImplementedError(f"This method has not been implemented for response type {type(response_from_direct_call)}")
        MonetaryCostManager.replace_predicted_usage_with_actual_usage_in_parent_managers(original_prediction, cost)


    @property
    def cost_per_token_completion(self) -> float:
        return self.caculate_cost_from_tokens(prompt_tkns=0, completion_tkns=1)


    @property
    def cost_per_token_prompt(self) -> float:
        return self.caculate_cost_from_tokens(prompt_tkns=1, completion_tkns=0)