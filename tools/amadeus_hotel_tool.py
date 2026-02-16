import sys
import requests
from typing import List
from langchain.tools import tool
from logger.logger import logger
from exception.exception_handling import TripMateException
from utils.amadeus_client import AmadeusClient


class AmadeusHotelTool:
    """
    This class is responsible for searching hotel availability using Amadeus.
    """

    def __init__(self):
        logger.info("Initializing AmadeusHotelTool")
        self.client = AmadeusClient()
        self.tool_list = self._setup_tools()

    def _setup_tools(self) -> List:

        @tool
        def search_hotels(city: str) -> str:
            """
            Search for available hotels in a city.
            Parameters will be:
            - city: 3-letter IATA city code (e.g., 'NYC', 'LON').
            """
            try:
                # Resolve City Code
                city_code = self.client.get_city_code(city)

                # Validation: Amadeus requires 3-letter IATA codes
                if len(city_code) != 3 or not city_code.isupper():
                    logger.warning(f"the invalid city code resolved: {city_code}")
                    return (
                        f"Hotel Search Failed: because it could not resolve '{city}' to a valid 3-letter IATA city code. "
                        "Please ask the user for the 3-letter city code (e.g., NYC, PAR) or try a to tell a specific city name."
                    )

                logger.info(
                    f"Searching for the hotels in {city_code} (resolved from '{city}') via Amadeus"
                )

                headers = self.client.get_headers()

                #Get Hotel List by City ---
                list_url = (
                    f"{self.client.base_url_v1}/reference-data/locations/hotels/by-city"
                )
                list_params = {"cityCode": city_code}

                list_response = requests.get(
                    list_url, headers=headers, params=list_params
                )

                if list_response.status_code != 200:
                    logger.error(f"Hotel List Error: {list_response.text}")
                    return f"Hotel Search is Failed: cos it can't find hotel IDs for {city_code}."

                hotel_data = list_response.json().get("data", [])
                if not hotel_data:
                    return f"No hotels found in the{city_code}. SYSTEM NOTE: If this is your second attempt, STOP and report failure to Supervisor."

                # Get top 3-5 hotel IDs
                hotel_ids = [h["hotelId"] for h in hotel_data[:10]]
                hotel_id_str = ",".join(hotel_ids)

                # Get Offers for those Hotels ---
                # Search by hotelIds is in V3
                offer_url = "https://test.api.amadeus.com/v3/shopping/hotel-offers"
                offer_params = {
                    "hotelIds": hotel_id_str,
                    "adults": 1,
                    "bestRateOnly": "true",
                }

                response = requests.get(offer_url, headers=headers, params=offer_params)

                if response.status_code == 200:
                    data = response.json()
                    offers = data.get("data", [])

                    if not offers:
                        return (
                            f"No live hotel offers found in {city_code} at this time."
                        )

                    results = []
                    for offer in offers:
                        name = offer.get("hotel", {}).get("name", "Unknown Hotel")
                        price = "N/A"
                        currency = "USD"

                        if "offers" in offer and len(offer["offers"]) > 0:
                            price_obj = offer["offers"][0].get("price", {})
                            price = price_obj.get("total", "N/A")
                            currency = price_obj.get("currency", "USD")

                        results.append(f"- {name}: {currency} {price}")

                    return f"Found hotel offers in {city_code}:\n" + "\n".join(results)

                elif response.status_code == 400:
                    logger.warning(f"Amadeus API Bad Request: {response.text}")
                    return f"Hotel Search Failed: Bad request when fetching offers for {city_code}."

                else:
                    logger.error(f"Amadeus API Error: {response.text}")
                    return f"Error searching hotels: {response.text}"

            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        return [search_hotels]
