from sl_ai_models.deepgram_nova2 import DeepgramNova2
from sl_ai_models.utils import file_manipulation
import asyncio
import logging
logger = logging.getLogger(__name__)


def test_deepgram_works_on_file_input() -> None:
    project_file_path = "tests/test_data/short-clip-buellers-life-moves-pretty-fast.wav"
    assert_deepgram_works_on_input(file_manipulation.get_absolute_path(project_file_path))


def test_deepgram_works_on_url() -> None:
    url = "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
    assert_deepgram_works_on_input(url)


def assert_deepgram_works_on_input(input: str) -> None:
    model = DeepgramNova2()
    response = asyncio.run(model.invoke(input))
    logger.debug(f"Response: {response}")
    assert response is not None, "Response is None"


