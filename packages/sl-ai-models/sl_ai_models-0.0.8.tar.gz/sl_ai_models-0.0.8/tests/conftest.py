# This file is run before any tests are run in order to configure tests

import pytest
from sl_ai_models.utils.custom_logger import CustomLogger

@pytest.fixture(scope="session", autouse=True)
def setup_logging() -> None:
    CustomLogger.set_up_logging()