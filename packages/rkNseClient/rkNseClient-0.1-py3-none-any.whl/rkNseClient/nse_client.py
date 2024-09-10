from datetime import datetime, timezone
from typing import Literal, Optional
import requests
import io
import pandas as pd
import numpy as np
from urllib.parse import urlparse, quote_plus
from requests.exceptions import HTTPError, Timeout, RequestException
from time import sleep
from .nse_schema import EquityInfoSchema


class NSEClient:
    def __init__(self, max_retries=3, retry_delay=2, rate_limit_delay=1):
        """
        Initialize the NseClientAPI with base configurations such as baseURL, user agent,
        and cookies. Set max_retries and delays for error handling and rate limiting.

        Args:
            max_retries (int): Max retries for requests in case of failures.
            retry_delay (int): Delay between retries in seconds.
            rate_limit_delay (int): Delay between successive requests to avoid rate limits.
        """
        self.baseURL = "https://www.nseindia.com/"
        self.userAgent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        self.cookies = {}
        self.equityQuotes = {}
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.rate_limit_delay = rate_limit_delay

        self.boardMarketIndicesList = [
            "Nifty 50",
            "Nifty Next 50",
            "Nifty 100",
            "Nifty 200",
            "Nifty Total Market",
            "Nifty 500",
            "Nifty 500 Multicap 50 25 25",
            "Nifty Midcap 150",
            "Nifty Midcap 50",
            "Nifty Midcap Select",
            "Nifty Midcap 100",
            "Nifty Smallcap 250",
            "Nifty Smallcap 50",
            "Nifty Smallcap 100",
            "Nifty Microcap 250",
            "Nifty Largemidcap 250",
            "Nifty Midsmallcap 400",
        ]
        self.sectorIndicesList = [
            "Nifty Auto Index",
            "Nifty Bank Index",
            "Nifty Financial Services Index",
            "Nifty Financial Services 25/50 Index",
            "Nifty Financial Services Ex-Bank index",
            "Nifty FMCG Index",
            "Nifty Healthcare Index",
            "Nifty IT Index",
            "Nifty Media Index",
            "Nifty Metal Index",
            "Nifty Pharma Index",
            "Nifty Private Bank Index",
            "Nifty PSU Bank Index",
            "Nifty Realty Index",
            "Nifty Consumer Durables Index",
            "Nifty Oil and Gas Index",
            "Nifty MidSmall Financial Services Index",
            "Nifty MidSmall Healthcare Index",
            "Nifty MidSmall IT & Telecom Index",
        ]
        self._initialRequest()

    def _equityUrlParser(self, url: str) -> str:
        """Encode URL parameters to handle special characters like '&'."""
        return url.replace("&", "%26")

    def _setCookies(self, response: requests.Response):
        """Update internal cookies from the response."""
        self.cookies.update(response.cookies.get_dict())

    def _initialRequest(self):
        """Send an initial request to set cookies and establish a session."""
        try:
            response = self._request_with_retries("GET", self.baseURL)
            self._setCookies(response=response)
        except RequestException as e:
            print(f"Error during initial request: {e}")

    def _request_with_retries(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Handle HTTP requests with retries and rate limiting.

        Args:
            method (str): HTTP method to use (GET, POST, etc.).
            url (str): URL to send the request to.

        Returns:
            requests.Response: The response object if successful.
        """
        retries = 0
        while retries < self.max_retries:
            try:
                sleep(self.rate_limit_delay)  # Apply rate limit delay
                response = requests.request(
                    method, url, headers={"User-Agent": self.userAgent}, **kwargs)
                response.raise_for_status()  # Raise HTTPError for bad responses
                return response
            except (HTTPError, Timeout) as e:
                retries += 1
                print(f"Attempt {retries}/{self.max_retries}: Error - {e}")
                sleep(self.retry_delay)
            except RequestException as e:
                raise Exception(f"Critical error: {e}")
        raise Exception(f"Failed after {self.max_retries} attempts.")

    def getEquityQuote(self, symbol: str) -> Optional[dict]:
        """
        Fetch equity quote information for a given symbol.

        Args:
            symbol (str): Stock symbol to fetch data for.

        Returns:
            dict: JSON response with equity quote data, or None if an error occurs.
        """
        try:
            url = f"https://www.nseindia.com/api/quote-equity?symbol={
                symbol.upper()}"
            response = self._request_with_retries(
                "GET", self._equityUrlParser(url), cookies=self.cookies, timeout=30)
            self._setCookies(response=response)
            self.equityQuotes = response.json()
            return self.equityQuotes
        except RequestException as e:
            print(f"Error fetching equity quote for {symbol}: {e}")
            return None

    def getEquityQuoteItem(self, itemName: Literal['info', 'metadata', 'securityInfo', 'sddDetails', 'priceInfo', 'industryInfo', 'preOpenMarket']) -> Optional[dict]:
        """
        Fetch specific item from the equity quotes data.

        Args:
            itemName (Literal): The key of the item to retrieve.

        Returns:
            dict: The requested item from equity quotes data, or raises an exception if empty.
        """
        if self.equityQuotes:
            return self.equityQuotes.get(itemName)
        else:
            raise ValueError(
                "Equity quotes data is empty. Fetch quotes using getEquityQuote().")

    def getFinalEquityQuote(self) -> dict:
        """
        Get the final processed equity quote with relevant fields.

        Returns:
            dict: Processed equity data with important fields.
        """
        stockInfo = self.getEquityQuoteItem("info")
        stockIndustryInfo = self.getEquityQuoteItem("industryInfo")
        stockMetaData = self.getEquityQuoteItem("metadata")
        stockSecurityInfo = self.getEquityQuoteItem("securityInfo")

        timezone_info = timezone.utc
        listingDate = self._parse_date(stockMetaData.get(
            "listingDate"), '%d-%b-%Y', timezone_info)
        lastUpdateTime = self._parse_date(
            stockMetaData.get("lastUpdateTime"), '%d-%b-%Y %H:%M:%S')

        return {
            "macro": str(stockIndustryInfo.get("macro")).strip(),
            "sector": str(stockIndustryInfo.get("sector")).strip(),
            "industry": str(stockIndustryInfo.get("industry")).strip(),
            "basicIndustry": str(stockIndustryInfo.get("basicIndustry")).strip(),
            "companyName": str(stockInfo.get("companyName")).strip(),
            "isin": stockMetaData.get("isin"),
            "symbol": stockMetaData.get("symbol"),
            "series": stockMetaData.get("series"),
            "status": stockMetaData.get("status"),
            "listingDate": listingDate,
            "pdSectorInd": str(stockMetaData.get("pdSectorInd")).strip(),
            "lastUpdateTime": lastUpdateTime,
            "faceValue": stockSecurityInfo.get("faceValue"),
            "issuedSize": stockSecurityInfo.get("issuedSize"),
        }

    def _parse_date(self, date_str: Optional[str], format_str: str, timezone_info=timezone.utc) -> Optional[datetime]:
        """
        Parse date strings into datetime objects.

        Args:
            date_str (str): Date string to parse.
            format_str (str): The format of the date string.

        Returns:
            Optional[datetime]: Parsed datetime object, or None if parsing fails.
        """
        if date_str:
            try:
                return datetime.strptime(date_str, format_str).replace(tzinfo=timezone_info)
            except ValueError as e:
                print(f"Date parsing error: {e}")
                return None
        return None

    def getEquityList(self) -> list[EquityInfoSchema]:
        """
        Fetch the equity list from NSE and return as a list of EquityInfoSchema objects.

        Returns:
            list[EquityInfoSchema]: List of equity information.
        """
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        try:
            response = self._request_with_retries(
                "GET", url, cookies=self.cookies, timeout=30)
            df = pd.read_csv(io.StringIO(response.text))
            df = df.replace({np.nan: None})
            equity_list = [
                EquityInfoSchema(
                    symbol=row["SYMBOL"],
                    nameOfCompany=row["NAME OF COMPANY"],
                    series=row[" SERIES"],
                    dateOfListing= row[" DATE OF LISTING"],
                    isinNumber=row[" ISIN NUMBER"],
                    faceValue=row[" FACE VALUE"],
                    paidUpValue=row[" PAID UP VALUE"],
                    marketLot=row[" MARKET LOT"]
                ) for _, row in df.iterrows()
            ]
            return equity_list
        except (pd.errors.ParserError, RequestException) as e:
            print(f"Error fetching equity list: {e}")
            return []

    def getBoardMarketIndicesList(self) -> list[str]:
        """
        Fetch the list of board market indices from the NSE.

        Returns:
            list[str]: A list of board market indices, or an empty list if an error occurs.
        """
        try:
            url = "https://www.nseindia.com/api/allIndices"
            response = self._request_with_retries(
                "GET", self._equityUrlParser(url), cookies=self.cookies, timeout=30)
            self._setCookies(response=response)
            data = response.json()

            indices_list = [
                index["indexName"] for index in data["data"]
                if index["indexName"] in self.boardMarketIndicesList
            ]
            return indices_list

        except RequestException as e:
            print(f"Error fetching board market indices: {e}")
            return []
        except (KeyError, TypeError) as e:
            print(f"Error processing board market indices data: {e}")
            return []

    def getSectoralIndicesList(self) -> list[str]:
        """
        Fetch the list of sectoral indices from the NSE.

        Returns:
            list[str]: A list of sectoral indices, or an empty list if an error occurs.
        """
        try:
            url = "https://www.nseindia.com/api/allIndices"
            response = self._request_with_retries(
                "GET", self._equityUrlParser(url), cookies=self.cookies, timeout=30)
            self._setCookies(response=response)
            data = response.json()

            indices_list = [
                index["indexName"] for index in data["data"]
                if index["indexName"] in self.sectorIndicesList
            ]
            return indices_list

        except RequestException as e:
            print(f"Error fetching sectoral indices: {e}")
            return []
        except (KeyError, TypeError) as e:
            print(f"Error processing sectoral indices data: {e}")
            return []
