import sys
import requests
from typing import List
from langchain.tools import tool
from logger.logger import logger
from exception.exception_handling import TripMateException
from utils.amadeus_client import AmadeusClient


class AmadeusTransportTool:
    """
    Tthis is a tools for searching transport options(flight primarily) using Amadeus API
    """

    def __init__(self):
        logger.info("Initializing AmadeusTransportTool")
        self.client = AmadeusClient()
        self.tool_list = self._setup_tools()

    def _setup_tools(self) -> List:

        @tool
        def search_transport(origin: str, destination: str, departure_date: str) -> str:
            """
            Search for flight options between two main cities.
            Parameters:
            - origin: 3-letter IATA code (e.g., 'BLR')
            - destination: 3-letter IATA code (e.g., 'YOW')
            - departure_date: Date in YYYY-MM-DD format (must be in the future).
            """
            try:
                # 1. Date Validation (Must be in the future)
                from datetime import datetime

                try:
                    search_date = datetime.strptime(departure_date, "%Y-%m-%d")
                    if search_date < datetime.now():
                        current_date = datetime.now().strftime("%Y-%m-%d")
                        return f"Transport Search Failed: because the date '{departure_date}' is in the past. TODAY IS {current_date}. Please use a future date."
                except ValueError:
                    return f"Transport Search Failed: Invalid date format '{departure_date}'. Please use YYYY-MM-DD."

                # 2. Origin/Destination Cleanup
                origin_code = self.client.get_city_code(origin)
                destination_code = self.client.get_city_code(destination)

                # 3. Origin/Destination Equality Check
                if origin_code == destination_code:
                    return f"Transport Search Failed: Origin and Destination are the same ({origin_code}). Please provide different locations."

                # 4. Validation: Amadeus requires 3-letter IATA codes
                if (
                    len(origin_code) != 3
                    or not origin_code.isupper()
                    or len(destination_code) != 3
                    or not destination_code.isupper()
                ):
                    logger.warning(
                        f"Invalid city codes resolved: {origin_code}, {destination_code}"
                    )
                    return (
                        f"Transport Search Failed: Could not resolve '{origin}' or '{destination}' to a valid 3-letter IATA code. "
                        "Please ask the user for the 3-letter airport codes (e.g., BLR, YYZ) to continue."
                    )

                logger.info(
                    f"Searching the transport from {origin_code} to {destination_code} on {departure_date}"
                )
                headers = self.client.get_headers()

                # endpoints for flight offers search
                url = f"{self.client.base_url}/shopping/flight-offers"

                params = {
                    "originLocationCode": origin_code,
                    "destinationLocationCode": destination_code,
                    "departureDate": departure_date,
                    "adults": 1,
                    "max": 5,
                    "currencyCode": "USD",
                }

                response = requests.get(url, headers=headers, params=params)

                if response.status_code == 200:
                    data = response.json()
                    offers = data.get("data", [])

                    if not offers:
                        return f"No direct transport found from {origin_code} to {destination_code} on {departure_date}. SYSTEM NOTE: If this is your second attempt, STOP and report failure to Supervisor."

                    results = []
                    for offer in offers:
                        price = offer.get("price", {}).get("total", "N/A")
                        currency = offer.get("price", {}).get("currency", "USD")

                        itineraries = offer.get("itineraries", [])
                        if itineraries:
                            segments = itineraries[0].get("segments", [])
                            route_summary = " -> ".join(
                                [
                                    f"{s['departure']['iataCode']}-{s['arrival']['iataCode']}"
                                    for s in segments
                                ]
                            )
                            duration = (
                                itineraries[0].get("duration", "N/A").replace("PT", "")
                            )

                            results.append(
                                f"- {route_summary} ({duration}): {currency} {price}"
                            )

                    return (
                        f"Found transport options for {departure_date}:\n"
                        + "\n".join(results)
                    )

                elif response.status_code == 400:
                    logger.warning(f"Amadeus API Bad Request: {response.text}")
                    return f"Transport Search Failed: Please check your Date ({departure_date}) and Locations. Dates must be in the future."

                else:
                    logger.error(f"Amadeus API Error: {response.text}")
                    return f"Error searching transport: {response.text}"

            except Exception as e:
                error = TripMateException(e, sys)
                logger.error(error.error_message)
                raise error

        return [search_transport]
