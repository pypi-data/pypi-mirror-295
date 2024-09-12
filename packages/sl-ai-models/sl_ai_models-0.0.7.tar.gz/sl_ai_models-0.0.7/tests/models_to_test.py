from sl_ai_models.gpt4ovision import Gpt4oVision
from sl_ai_models.gpt4o import Gpt4o
from sl_ai_models.perplexity import Perplexity
from sl_ai_models.claude35sonnet import Claude35Sonnet
from sl_ai_models.exa_searcher import ExaSearcher
from sl_ai_models.gpt4omini import Gpt4oMini
from sl_ai_models.deepgram_nova2 import DeepgramNova2

from sl_ai_models.basic_model_interfaces.token_limited_model import TokenLimitedModel
from sl_ai_models.basic_model_interfaces.retryable_model import RetryableModel
from sl_ai_models.basic_model_interfaces.time_limited_model import TimeLimitedModel
from sl_ai_models.basic_model_interfaces.request_limited_model import RequestLimitedModel
from sl_ai_models.basic_model_interfaces.incurs_cost import IncursCost
from sl_ai_models.basic_model_interfaces.ai_model import AiModel
from sl_ai_models.basic_model_interfaces.outputs_text import OutputsText
from sl_ai_models.basic_model_interfaces.tokens_incur_cost import TokensIncurCost


class ModelsToTest:
    ALL_MODELS = [
        Gpt4o,
        Gpt4oMini,
        Gpt4oVision,
        Perplexity,
        Claude35Sonnet,
        ExaSearcher,
        DeepgramNova2,
    ]
    BASIC_MODEL_LIST: list[type[AiModel]] = [model for model in ALL_MODELS if issubclass(model, AiModel)]
    RETRYABLE_LIST: list[type[RetryableModel]] = [model for model in ALL_MODELS if issubclass(model, RetryableModel)]
    TIME_LIMITED_LIST: list[type[TimeLimitedModel]] = [model for model in ALL_MODELS if issubclass(model, TimeLimitedModel)]
    REQUEST_LIMITED_LIST: list[type[RequestLimitedModel]] = [model for model in ALL_MODELS if issubclass(model, RequestLimitedModel)]
    TOKEN_LIMITED_LIST: list[type[TokenLimitedModel]] = [model for model in ALL_MODELS if issubclass(model, TokenLimitedModel)]
    INCURS_COST_LIST: list[type[IncursCost]] = [model for model in ALL_MODELS if issubclass(model, IncursCost)]
    OUTPUTS_TEXT: list[type[OutputsText]] = [model for model in ALL_MODELS if issubclass(model, OutputsText)]
    TOKENS_INCUR_COST_LIST: list[type[TokensIncurCost]] = [model for model in ALL_MODELS if issubclass(model, TokensIncurCost)]

