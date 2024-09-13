import sys
from pathlib import Path
import random
import json
import re
import feedparser
import pandas as pd
import asyncio
import datetime
from _asyncpg.asyncpg_sdk import AsyncpgSDK
import httpx
import asyncio
from bs4 import BeautifulSoup
import aiohttp
import xml.etree.ElementTree as ET
class SECSdk:
    def __init__(self):
        self.inline_filings_url=f"https://www.sec.gov/Archives/edgar/usgaap.rss.xml"
        self.headers = { 
            'User-Agent': 'fudstop AdminContact@fudstop.io',
            "Accept-Encoding": "gzip, deflate",
            'Host': 'www.sec.gov'
        }
        self.base_url = f"https://www.sec.gov"
        self.db = AsyncpgSDK(host='localhost', user='chuck', database='market_data', password='fud', port=5432)
        self.ticker_df = pd.read_csv('files/ciks.csv')
        self.ns = {'atom': 'http://www.w3.org/2005/Atom'}
        self.amc_rss = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001411579&type=&dateb=&owner=include&start=0&count=40&output=atom"
    async def fetch_data(self, url):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return None
    async def parse_data(self, xml_data):
        root = ET.fromstring(xml_data)
        data = []

        # Iterate over each entry in the XML
        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            updated = entry.find('{http://www.w3.org/2005/Atom}updated').text

            # Navigate to the content tag where filing details are located
            content = entry.find('{http://www.w3.org/2005/Atom}content')

            # Access each element using the correct paths
            accession_number = content.find('{http://www.w3.org/2005/Atom}accession-number').text if content.find('{http://www.w3.org/2005/Atom}accession-number') is not None else None
            filing_type = content.find('{http://www.w3.org/2005/Atom}filing-type').text if content.find('{http://www.w3.org/2005/Atom}filing-type') is not None else None
            filing_date = content.find('{http://www.w3.org/2005/Atom}filing-date').text if content.find('{http://www.w3.org/2005/Atom}filing-date') is not None else None
            film_number = content.find('{http://www.w3.org/2005/Atom}film-number').text if content.find('{http://www.w3.org/2005/Atom}film-number') is not None else None
            size = content.find('{http://www.w3.org/2005/Atom}size').text if content.find('{http://www.w3.org/2005/Atom}size') is not None else None
            form_name = content.find('{http://www.w3.org/2005/Atom}form-name').text if content.find('{http://www.w3.org/2005/Atom}form-name') is not None else None

            # The link element might be inside content, explicitly find it using a different path
            filing_link = content.find('.//{http://www.w3.org/2005/Atom}filing-href').text if content.find('.//{http://www.w3.org/2005/Atom}filing-href') is not None else None
            print(filing_link)
            data.append({
                "Title": title,
                "Updated": updated,
                "Accession Number": accession_number,
                "Filing Type": filing_type,
                "Filing Date": filing_date,
                "Film Number": film_number,
                "Size": size,
                "Form Name": form_name,
                "Filing Link": filing_link
            })

        df = pd.DataFrame(data)
        return df


    def get_cik_by_ticker(self, df, ticker):

        row = df[df['ticker'] == ticker]
        if not row.empty:
            return row.iloc[0]['cik']
        else:
            return None
    def get_ticker_by_cik(self, df, cik):
        # Search the DataFrame for the given CIK
        row = df[df['cik'] == cik]
        
        # If a matching row is found, return the ticker symbol
        if not row.empty:
            return row.iloc[0]['ticker']
        
        # If no matching row is found, return None
        else:
            return None
        
    # Function to extract filing links (already defined)
    def extract_filing_links(self, df):
        titles = df['Title'].tolist()
        dates = df['Filing Date'].tolist()
        links = df['Filing Link'].tolist()  # Assuming you've included this in the DataFrame

        # Return the extracted data
        return pd.DataFrame({
            'Title': titles,
            'Filing Date': dates,
            'Link': links
        })
    # Fetch details for each filing link
    async def fetch_filing_details(self, session, link):
        async with session.get(link) as response:
            if response.status == 200:
                html_content = await response.text()
                return html_content
            return None

    async def get_sec_filings(self, url=None):
        if url == None:
            url = self.amc_rss
        data = await self.fetch_data(url)
        parsed_data = await self.parse_data(data)

        return parsed_data
  