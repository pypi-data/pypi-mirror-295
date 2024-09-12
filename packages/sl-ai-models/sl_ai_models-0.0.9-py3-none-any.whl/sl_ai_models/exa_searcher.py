from __future__ import annotations

from sl_ai_models.utils.jsonable import Jsonable
from sl_ai_models.basic_model_interfaces.request_limited_model import RequestLimitedModel
from sl_ai_models.basic_model_interfaces.retryable_model import RetryableModel
from sl_ai_models.basic_model_interfaces.time_limited_model import TimeLimitedModel
from sl_ai_models.basic_model_interfaces.priced_per_request import PricedPerRequest
from sl_ai_models.basic_model_interfaces.incurs_cost import IncursCost
from sl_ai_models.resource_managers.monetary_cost_manager import MonetaryCostManager, UsagePrediction

from pydantic import BaseModel
import os
import aiohttp
import logging
logger = logging.getLogger(__name__)


class ExaSource(BaseModel, Jsonable):
    original_query: str
    auto_prompt_string: str | None
    title: str | None
    url: str | None
    text: str | None
    author: str | None
    published_date: str | None
    score: float | None
    highlights: list[str]
    highlight_scores: list[float]


class ExaSearcher(RequestLimitedModel, RetryableModel, TimeLimitedModel, IncursCost, PricedPerRequest):
    REQUESTS_PER_PERIOD_LIMIT = 25 # 25 is a guess from manual experimentation since they don't seem to publish this in an obvious place
    REQUEST_PERIOD_IN_SECONDS = 60
    TIMEOUT_TIME = 30
    PRICE_PER_REQUEST = 0.005


    async def invoke(self, search_query: str) -> list[ExaSource]:
        return await self.__retryable_timed_cost_request_limited_invoke(search_query)


    @RetryableModel._retry_according_to_model_allowed_tries
    @RequestLimitedModel._wait_till_request_capacity_available
    @IncursCost._wrap_in_cost_limiting_and_tracking
    @TimeLimitedModel._wrap_in_model_defined_timeout
    async def __retryable_timed_cost_request_limited_invoke(self, search_query: str) -> list[ExaSource]:
        response = await self._mockable_direct_call_to_model(search_query)
        return response


    async def _mockable_direct_call_to_model(self, search_query: str) -> list[ExaSource]:
        self._everything_special_to_call_before_direct_call()
        api_key = os.getenv("EXA_API_KEY")
        assert api_key is not None, "EXA_API_KEY is not set in the environment variables"
        url = "https://api.exa.ai/search"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key
        }
        payload = {
            "query": search_query,
            "type": "neural",
            "useAutoprompt": True,
            "numResults": 20,
            "contents": {
            "text": {
                "includeHtmlTags": True
            },
            "highlights": {
                "numSentences": 4,
                "highlightsPerUrl": 10,
                "query": search_query
            },
            "summary": True
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response.raise_for_status()
                response_data: dict = await response.json()


        exa_sources: list[ExaSource] = []
        auto_prompt_string = response_data.get("autopromptString")
        for result in response_data["results"]:
            result: dict
            exa_source = ExaSource(
                original_query=search_query,
                auto_prompt_string=auto_prompt_string,
                title=result.get("title"),
                url=result.get("url"),
                text=result.get("text"),
                author=result.get("author"),
                published_date=result.get("publishedDate"),
                score=result.get("score"),
                highlights=result.get("highlights", []),
                highlight_scores=result.get("highlightScores", [])
            )
            exa_sources.append(exa_source)

        logger.debug(f"Exa API returned {len(exa_sources)} sources with urls: {[source.url for source in exa_sources]}")
        return exa_sources


    def _estimate_before_plus_after_cost_from_model_input(self, search_query: str) -> float:
        return self.PRICE_PER_REQUEST


    async def _track_cost_in_manager_using_model_response(self, response_from_direct_call: list[ExaSource], original_cost_prediction: UsagePrediction) -> None:
        assert isinstance(response_from_direct_call, list), f"response_from_direct_call is not a list, it is a {type(response_from_direct_call)}"
        cost = self.PRICE_PER_REQUEST
        MonetaryCostManager.replace_predicted_usage_with_actual_usage_in_parent_managers(original_cost_prediction, cost)


    @staticmethod
    def _get_mock_return_for_direct_call_to_model_using_cheap_input() -> list[ExaSource]:
        return [
            ExaSource(
                original_query="Moko Research Website",
                auto_prompt_string="Here is a link to the Moko Research website:",
                title="MokoResearch",
                url="https://www.mokoresearch.com",
                text="Fake text",
                author=None,
                published_date=None,
                score=0.99,
                highlights=[],
                highlight_scores=[],
            )
        ]


    @staticmethod
    def _get_cheap_input_for_invoke() -> str:
        return "MokoResearch Website"


# Example response from Exa API: (see the Exa playground for more examples)
# ... other data ... below is first source in "results" list
# {
#   "score": 0.19072401523590088,
#   "title": "Assassinated Presidents Archives - History",
#   "id": "https://www.historyonthenet.com/category/assassinated-presidents",
#   "url": "https://www.historyonthenet.com/category/assassinated-presidents",
#   "publishedDate": "2019-01-01T00:00:00.000Z",
#   "author": "None",
#   "text": "<div><div> <div> <p>Scroll down to see articles about the U.S. presidents who died in office, and the backgrounds and motivations of their assassins</p> </div> <p>Scroll down to see articles about the U.S. presidents who died in office, and the backgrounds and motivations of their assassins</p> <hr /> <article> <a href=\"https://www.historyonthenet.com/oscar-ramiro-ortega-hernandez\"> </a> <h2><a href=\"https://www.historyonthenet.com/oscar-ramiro-ortega-hernandez\">Oscar Ramiro Ortega-Hernandez</a></h2> <p>The following article on Oscar Ramiro Ortega-Hernandez is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. Perhaps the most dangerous threat to President Obama’s life came from twenty-one-year-old Oscar Ramiro Ortega-Hernandez, who had criminal…</p> </article> <article> <a href=\"https://www.historyonthenet.com/copycat-killers\"> </a> <h2><a href=\"https://www.historyonthenet.com/copycat-killers\">Copycat Killers: Becoming Famous by Becoming Infamous</a></h2> <p>The following article on copycat killers is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. Many assassins and would-be assassins of U.S. presidents were copycat killers obsessed with assassins from the past. Some borrowed…</p> </article> <article> <a href=\"https://www.historyonthenet.com/assassinated-presidents\"> </a> <h2><a href=\"https://www.historyonthenet.com/assassinated-presidents\">Assassinated Presidents: Profiles of Them and Their Killers</a></h2> <p>The following article on assassinated presidents is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. The list of assassinated presidents receives a new member approximately every 20-40 years. Here are those who were killed while…</p> </article> <article> <a href=\"https://www.historyonthenet.com/isaac-aguigui\"> </a> <h2><a href=\"https://www.historyonthenet.com/isaac-aguigui\">Isaac Aguigui: Militia Leader, Wannabe Presidential Assassin</a></h2> <p>The following article on Isaac Aguigui is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. In 2012, Barack Obama was targeted by a domestic terror group of soldiers called F.E.A.R. (“Forever Enduring Always Read”),…</p> </article> <article> <a href=\"https://www.historyonthenet.com/khalid-kelly\"> </a> <h2><a href=\"https://www.historyonthenet.com/khalid-kelly\">Khalid Kelly: Irish Would-Be Obama Assassin</a></h2> <p>The following article on Terry Kelly (\"Khalid Kelly\") is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. In May 2011, Irish Muslim militant Terry “Khalid” Kelly was arrested for threatening to assassinate President…</p> </article> <article> <a href=\"https://www.historyonthenet.com/timothy-ryan-gutierrez-hacker-threatened-obama\"> </a> <h2><a href=\"https://www.historyonthenet.com/timothy-ryan-g",
#   "highlights": [
#     "The list of assassinated presidents receives a new member approximately every 20-40 years. Here are those who were killed while…      Isaac Aguigui: Militia Leader, Wannabe Presidential Assassin  The following article on Isaac Aguigui is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. In 2012, Barack Obama was targeted by a domestic terror group of soldiers called F.E.A.R.",
#     "In 2012, Barack Obama was targeted by a domestic terror group of soldiers called F.E.A.R. (“Forever Enduring Always Read”),…      Khalid Kelly: Irish Would-Be Obama Assassin  The following article on Terry Kelly (\"Khalid Kelly\") is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. In May 2011, Irish Muslim militant Terry “Khalid” Kelly was arrested for threatening to assassinate President…",
#     "Here are those who were killed while…      Isaac Aguigui: Militia Leader, Wannabe Presidential Assassin  The following article on Isaac Aguigui is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. In 2012, Barack Obama was targeted by a domestic terror group of soldiers called F.E.A.R. (“Forever Enduring Always Read”),…      Khalid Kelly: Irish Would-Be Obama Assassin  The following article on Terry Kelly (\"Khalid Kelly\") is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama.",
#     "It is available for order now from Amazon and Barnes &amp; Noble. The list of assassinated presidents receives a new member approximately every 20-40 years. Here are those who were killed while…      Isaac Aguigui: Militia Leader, Wannabe Presidential Assassin  The following article on Isaac Aguigui is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble.",
#     "In May 2011, Irish Muslim militant Terry “Khalid” Kelly was arrested for threatening to assassinate President…",
#     "Perhaps the most dangerous threat to President Obama’s life came from twenty-one-year-old Oscar Ramiro Ortega-Hernandez, who had criminal…      Copycat Killers: Becoming Famous by Becoming Infamous  The following article on copycat killers is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. Many assassins and would-be assassins of U.S. presidents were copycat killers obsessed with assassins from the past. Some borrowed…      Assassinated Presidents: Profiles of Them and Their Killers  The following article on assassinated presidents is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama.",
#     "It is available for order now from Amazon and Barnes &amp; Noble. In 2012, Barack Obama was targeted by a domestic terror group of soldiers called F.E.A.R. (“Forever Enduring Always Read”),…      Khalid Kelly: Irish Would-Be Obama Assassin  The following article on Terry Kelly (\"Khalid Kelly\") is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble.",
#     "Many assassins and would-be assassins of U.S. presidents were copycat killers obsessed with assassins from the past. Some borrowed…      Assassinated Presidents: Profiles of Them and Their Killers  The following article on assassinated presidents is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. The list of assassinated presidents receives a new member approximately every 20-40 years.",
#     "It is available for order now from Amazon and Barnes &amp; Noble. Many assassins and would-be assassins of U.S. presidents were copycat killers obsessed with assassins from the past. Some borrowed…      Assassinated Presidents: Profiles of Them and Their Killers  The following article on assassinated presidents is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble.",
#     "Some borrowed…      Assassinated Presidents: Profiles of Them and Their Killers  The following article on assassinated presidents is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama. It is available for order now from Amazon and Barnes &amp; Noble. The list of assassinated presidents receives a new member approximately every 20-40 years. Here are those who were killed while…      Isaac Aguigui: Militia Leader, Wannabe Presidential Assassin  The following article on Isaac Aguigui is an excerpt from Mel Ayton's Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama."
#   ],
#   "highlightScores": [
#     0.10017715394496918,
#     0.0916084423661232,
#     0.08568621426820755,
#     0.08466880768537521,
#     0.08453669399023056,
#     0.08243578672409058,
#     0.08049978315830231,
#     0.08013768494129181,
#     0.0784364566206932,
#     0.07647785544395447
#   ],
#   "summary": "This webpage is a collection of articles about U.S. presidents who died in office, and the backgrounds and motivations of their assassins. It includes excerpts from the book \"Hunting the President: Threats, Plots, and Assassination Attempts—From FDR to Obama\" by Mel Ayton. The articles cover a variety of topics, including the assassination attempt on President Obama by Oscar Ramiro Ortega-Hernandez, the motivations of copycat killers, and the various individuals who have attempted to assassinate U.S. presidents throughout history. \n"
# }