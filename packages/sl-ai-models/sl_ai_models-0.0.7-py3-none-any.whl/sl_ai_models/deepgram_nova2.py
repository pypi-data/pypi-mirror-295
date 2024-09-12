
from sl_ai_models.model_archetypes.deepgram_model import DeepgramAudioToTextModel, DeepgramOutput #NOSONAR # Keep DeepgramOutput here for easier imports
from typing import Final

class DeepgramNova2(DeepgramAudioToTextModel):
    MODEL_NAME: Final[str] = "nova-2"
    TIMEOUT_TIME: Final[int] = 85
    REQUESTS_PER_PERIOD_LIMIT: Final[int] = 100 # Technically its that you can only have 100 concurrent requests, but its easier to reuse rate limiting https://developers.deepgram.com/reference/api-rate-limits
    REQUEST_PERIOD_IN_SECONDS: Final[int] = 90
