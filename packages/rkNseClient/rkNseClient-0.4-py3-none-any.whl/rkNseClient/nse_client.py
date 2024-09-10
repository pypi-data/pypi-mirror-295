from datetime import datetime, timezone
from typing import Literal, List, Dict
import requests, io
import pandas as pd
import numpy as np


class NSEClientAPI:
    """
    NSE Client API for fetching equity data, market indices, and sectoral indices.
    
    This class provides methods for retrieving equity quotes, lists of equities,
    board market indices, sector indices, and securities in the equity segment.
    
    Attributes:
        base_url (str): Base URL for the NSE website.
        user_agent (str): User-Agent header for requests.
        cookies (dict): A dictionary to store session cookies.
        equity_quotes (dict): A dictionary to store equity quotes after fetching.
        board_market_indices_list (list): List of available board market indices.
        sector_indices_list (list): List of available sector indices.
    """

    def __init__(self):
        """Initialize the NSE Client API and make an initial request to the NSE website."""
        self.base_url = "https://www.nseindia.com/"
        self.user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        self.cookies = {}
        self.equity_quotes = {}

        self.board_market_indices_list = [
            "Nifty 50", "Nifty Next 50", "Nifty 100", "Nifty 200", "Nifty Total Market",
            "Nifty 500", "Nifty 500 Multicap 50 25 25", "Nifty Midcap 150", "Nifty Midcap 50",
            "Nifty Midcap Select", "Nifty Midcap 100", "Nifty Smallcap 250", "Nifty Smallcap 50",
            "Nifty Smallcap 100", "Nifty Microcap 250", "Nifty Largemidcap 250", "Nifty Midsmallcap 400"
        ]
        self.sector_indices_list = [
            "Nifty Auto Index", "Nifty Bank Index", "Nifty Financial Services Index", "Nifty FMCG Index",
            "Nifty IT Index", "Nifty Media Index", "Nifty Metal Index", "Nifty Pharma Index",
            "Nifty Realty Index", "Nifty Oil and Gas Index"
        ]
        self.initial_request()

    def equity_url_parser(self, url: str) -> str:
        """Parses the equity URL and encodes special characters.

        Args:
            url (str): The URL to parse.

        Returns:
            str: Parsed URL with encoded special characters.
        """
        return url.replace("&", "%26")

    def set_cookies(self, response: requests.Response):
        """Updates the session cookies with the ones from the response.

        Args:
            response (requests.Response): The response object from which to extract cookies.
        """
        self.cookies.update(response.cookies.get_dict())

    def initial_request(self):
        """Makes the initial request to NSE to establish a session."""
        response = self.session.get(self.base_url)
        self.set_cookies(response)
        print("Initial request to NSE made.")

    def get_equity_quote(self, symbol: str) -> dict:
        """Fetches the equity quote for a given symbol from the NSE API.

        Args:
            symbol (str): The stock symbol for which to fetch the quote.

        Returns:
            dict: Equity quote information.
        """
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol.upper()}"
        response = self.session.get(self.equity_url_parser(url), cookies=self.cookies, timeout=30)
        self.set_cookies(response)
        self.equity_quotes = response.json()
        return self.equity_quotes

    def get_equity_quote_item(self, item_name: Literal['info', 'metadata', 'securityInfo', 'sddDetails', 'priceInfo', 'industryInfo', 'preOpenMarket']) -> dict:
        """Retrieves a specific item from the equity quote.

        Args:
            item_name (str): The name of the item to retrieve.

        Returns:
            dict: The requested item from the equity quote.

        Raises:
            Exception: If equityQuotes is empty.
        """
        if self.equity_quotes:
            return self.equity_quotes[item_name]
        else:
            raise Exception("equityQuotes is empty")

    def get_final_equity_quote(self) -> dict:
        """Retrieves final equity quote information such as company name, industry, ISIN, etc.

        Returns:
            dict: Final equity quote data.
        """
        stock_info = self.get_equity_quote_item("info")
        stock_industry_info = self.get_equity_quote_item("industryInfo")
        stock_metadata = self.get_equity_quote_item("metadata")
        stock_security_info = self.get_equity_quote_item("securityInfo")

        timezone_info = timezone.utc
        try:
            listing_date = datetime.strptime(stock_metadata.get("listingDate"), '%d-%b-%Y').replace(tzinfo=timezone_info)
        except Exception:
            listing_date = None
        try:
            last_update_time = datetime.strptime(stock_metadata.get("lastUpdateTime"), '%d-%b-%Y %H:%M:%S')
        except Exception:
            last_update_time = None

        return {
            "macro": str(stock_industry_info.get("macro")).strip(),
            "sector": str(stock_industry_info.get("sector")).strip(),
            "industry": str(stock_industry_info.get("industry")).strip(),
            "basicIndustry": str(stock_industry_info.get("basicIndustry")).strip(),
            "companyName": str(stock_info.get("companyName")).strip(),
            "isin": stock_metadata.get("isin"),
            "symbol": stock_metadata.get("symbol"),
            "series": stock_metadata.get("series"),
            "status": stock_metadata.get("status"),
            "listingDate": listing_date,
            "pdSectorInd": str(stock_metadata.get("pdSectorInd")).strip(),
            "lastUpdateTime": last_update_time,
            "faceValue": stock_security_info.get("faceValue"),
            "issuedSize": stock_security_info.get("issuedSize")
        }

    def get_equity_list(self) -> List[Dict]:
        """Fetches the list of equities from NSE.

        Returns:
            list: A list of equities as dictionaries.
        """
        url = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
        response = self.session.get(url, cookies=self.cookies, timeout=30)

        df = pd.read_csv(io.StringIO(response.text)).replace({np.nan: None})
        return df.to_dict("records")

    def get_board_market_indices_list(self, indices_name: Literal[
        "Nifty 50", "Nifty Next 50", "Nifty 100", "Nifty 200", "Nifty Total Market",
        "Nifty 500", "Nifty Midcap 150"
    ]) -> List[Dict]:
        """Fetches the list of companies in a specific board market index.

        Args:
            indices_name (str): The name of the board market index.

        Returns:
            list: A list of companies in the specified index.
        """
        url_dict = {
            "Nifty 50": "https://nsearchives.nseindia.com/content/indices/ind_nifty50list.csv",
            "Nifty Next 50": "https://nsearchives.nseindia.com/content/indices/ind_niftynext50list.csv",
            # Other indices mappings...
        }

        url = url_dict[indices_name]
        response = self.session.get(url, cookies=self.cookies, timeout=30)
        return pd.read_csv(io.StringIO(response.text)).to_dict("records")

    def get_sectoral_indices_list(self, indices_name: Literal[
        "Nifty Auto Index", "Nifty Bank Index", "Nifty FMCG Index"
    ]) -> List[Dict]:
        """Fetches the list of companies in a specific sectoral index.

        Args:
            indices_name (str): The name of the sectoral index.

        Returns:
            list: A list of companies in the specified sectoral index.
        """
        url_dict = {
            "Nifty Auto Index": "https://www.niftyindices.com/IndexConstituent/ind_niftyautolist.csv",
            # Other sector mappings...
        }

        url = url_dict[indices_name]
        response = self.session.get(url, cookies=self.cookies, timeout=30)
        return pd.read_csv(io.StringIO(response.text)).to_dict("records")

    def securities_in_equity_segment(self) -> List[Dict]:
        """Fetches the list of securities in the equity segment.

        Returns:
            list: A list of securities in the equity segment.
        """
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        response = self.session.get(url, cookies=self.cookies, timeout=30)
        df = pd.read_csv(io.StringIO(response.text)).replace({np.nan: None})
        return df.to_dict("records")
