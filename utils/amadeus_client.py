import os
import sys
import time
import requests

from dotenv import load_dotenv
from logger.logger import logger
from exception.exception_handling import TripMateException


class AmadeusClient:
    """
    A singleton wrapper for the Amadeus API client to hanlde the auth and base request
    """

    _instance = None
    _token = None
    _token_expires = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AmadeusClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Load the creadentials and setup sessions
        """
        load_dotenv()
        self.client_id = os.getenv("AMADEUS_API_KEY")
        self.client_secret = os.getenv("AMADEUS_API_SECRET")
        self.base_url = "https://test.api.amadeus.com/v2"
        self.base_url_v1 = "https://test.api.amadeus.com/v1"

        if not self.client_id or not self.client_secret:
            logger.warning("Amadeus API credentials not found")

    def _get_token(self):
        """
        Get the access token for the Amadeus API
        """
        if self._token and self._token_expires and time.time() < self._token_expires:
            return self._token

        try:
            logger.info("Authenticating with Amadeus API")

            auth_url = "https://test.api.amadeus.com/v1/security/oauth2/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

            response = requests.post(auth_url, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self._token = token_data["access_token"]
            self._token_expires = time.time() + token_data["expires_in"] - 60
            return self._token

        except Exception as e:
            error = TripMateException(e, sys)
            logger.error(error.error_message)
            raise error

    def get_headers(self):
        """
        Returns authorization headers for API calls.
        """
        token = self._get_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def get_city_code(self, keyword: str) -> str:
        """
        Resolves a city name (e.g., "New York") to its IATA code (e.g., "NYC").
        Uses the Amadeus Location API dynamically.
        """
        try:
            logger.info(f"Resolving city code for: {keyword}")

            # 1. Normalization for common name variations (Dynamic aliases)
            keyword = keyword.strip()
            aliases = {
                "bangalore": "Bengaluru",
                "mumbai": "Bombay",
                "chennai": "Madras",
                "kolkata": "Calcutta",
            }
            if keyword.lower() in aliases:
                keyword = aliases[keyword.lower()]

            # 2. If it's already a 3-letter uppercase code, return it directly
            if len(keyword) == 3 and keyword.isupper():
                return keyword

            # 3. Extract code from parenthesis if present, e.g., "Bengaluru (BLR)" -> "BLR"
            import re

            match = re.search(r"\(([A-Z]{3})\)", keyword)
            if match:
                return match.group(1)

            # 4. Dynamic API Resolution (Must use V1 endpoint)
            headers = self.get_headers()
            url = f"{self.base_url_v1}/reference-data/locations"

            # Use both CITY and AIRPORT to catch the most relevant IATA codes
            params = {
                "subType": "CITY,AIRPORT",
                "keyword": keyword.upper(),
                "view": "LIGHT",
                "sort": "analytics.travelers.score",  # Order by popularity to get the main hub first
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json().get("data", [])
                if data:
                    # Logic: Look for the first item that has a valid 3-letter iataCode
                    for item in data:
                        code = item.get("iataCode") or item.get("iata_code")
                        if code and len(code) == 3:
                            logger.info(
                                f"Dynamic resolution successful: {keyword} -> {code}"
                            )
                            return code

            logger.warning(
                f"Dynamic resolution failed for '{keyword}'. Returning input as-is."
            )
            return keyword

        except Exception as e:
            logger.error(f"Error resolving city code: {e}")
            return keyword
