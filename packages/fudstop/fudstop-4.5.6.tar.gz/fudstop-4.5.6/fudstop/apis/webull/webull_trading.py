import time
from dotenv import load_dotenv
load_dotenv()
import ta.volatility
import ta.volume
from webull import webull as wb
import aiohttp
import ta
import httpx
import pandas as pd
from pytz import timezone
from .webull_helpers import calculate_countdown, calculate_setup
from .trade_models.stock_quote import MultiQuote
from .trade_models.capital_flow import CapitalFlow, CapitalFlowHistory
from .trade_models.deals import Deals
from .trade_models.cost_distribution import CostDistribution, NewCostDist
from .trade_models.etf_holdings import ETFHoldings
from .trade_models.institutional_holdings import InstitutionHolding, InstitutionStat
from .trade_models.financials import BalanceSheet, FinancialStatement, CashFlow
from .trade_models.news import NewsItem
from .trade_models.forecast_evaluator import ForecastEvaluator
from .trade_models.short_interest import ShortInterest
from fudstop.apis.webull.webull_option_screener import WebullOptionScreener
from .trade_models.volume_analysis import WebullVolAnalysis
from .trade_models.ticker_query import WebullStockData
from .trade_models.analyst_ratings import Analysis
from .trade_models.price_streamer import PriceStreamer
from .trade_models.company_brief import CompanyBrief, Executives, Sectors
from .trade_models.order_flow import OrderFlow
import asyncio
import ta
from datetime import datetime, timedelta, timezone

screen = WebullOptionScreener()
webull = wb()
class WebullTrading:
    def __init__(self):
        self.most_active_tickers= ['SNOW', 'IBM', 'DKNG', 'SLV', 'NWL', 'SPXS', 'DIA', 'QCOM', 'CMG', 'WYNN', 'PENN', 'HLF', 'CCJ', 'WW', 'NEM', 'MOS', 'SRPT', 'MS', 'DPST', 'AG', 'PAA', 'PANW', 'XPEV', 'BHC', 'KSS', 'XLP', 'LLY', 'MDB', 'AZN', 'NVO', 'BOIL', 'ZM', 'HUT', 'VIX', 'PDD', 'SLB', 'PCG', 'DIS', 'TFC', 'SIRI', 'TDOC', 'CRSP', 'BSX', 'BITF', 'AAL', 'EOSE', 'RIVN', 'X', 'CCL', 'SOXS', 'NOVA', 'TMUS', 'HES', 'LI', 'NVAX', 'TSM', 'CNC', 'IAU', 'GDDY', 'CVX', 'TGT', 'MCD', 'GDXJ', 'AAPL', 'NKLA', 'EDR', 'NOK', 'SPWR', 'NKE', 'HYG', 'FSLR', 'SGEN', 'DNN', 'BAX', 'CRWD', 'OSTK', 'XLC', 'RIG', 'SEDG', 'SNDL', 'RSP', 'M', 'CD', 'UNG', 'LQD', 'TTD', 'AMGN', 'EQT', 'YINN', 'MULN', 'FTNT', 'WBD', 'MRNA', 'PTON', 'SCHW', 'ABNB', 'EW', 'PM', 'UCO', 'TXN', 'DLR', 'KHC', 'MMAT', 'QQQ', 'GOOGL', 'AEM', 'RTX', 'AVGO', 'RBLX', 'PAAS', 'UUP', 'OXY', 'SQ', 'PLUG', 'CLF', 'GOEV', 'BKLN', 'ALB', 'BALL', 'SMH', 'CVE', 'F', 'KRE', 'TWLO', 'ARCC', 'ARM', 'U', 'SOFI', 'SBUX', 'FXI', 'BMY', 'HSBC', 'EFA', 'SVXY', 'VALE', 'GOLD', 'MSFT', 'OIH', 'ARKK', 'AMD', 'AA', 'DXCM', 'ABT', 'WOLF', 'FDX', 'SOXL', 'MA', 'KWEB', 'BP', 'SNAP', 'NLY', 'KGC', 'URA', 'UVIX', 'KMI', 'ACB', 'NET', 'W', 'GRAB', 'LMT', 'EPD', 'FCX', 'STNE', 'NIO', 'SU', 'ET', 'CVS', 'ADBE', 'MXL', 'HOOD', 'FUBO', 'RIOT', 'CRM', 'TNA', 'DISH', 'XBI', 'VFS', 'GPS', 'NVDA', 'MGM', 'MRK', 'ABBV', 'LABU', 'BEKE', 'VRT', 'LVS', 'CPNG', 'BA', 'MTCH', 'PEP', 'EBAY', 'GDX', 'XLV', 'UBER', 'GOOG', 'COF', 'XLU', 'BILI', 'XLK', 'VXX', 'DVN', 'MSOS', 'KOLD', 'XOM', 'BKNG', 'SPY', 'RUT', 'CMCSA', 'STLA', 'NCLH', 'GRPN', 'ZION', 'UAL', 'GM', 'NDX', 'TQQQ', 'COIN', 'WBA', 'CLSK', 'NFLX', 'FREY', 'AFRM', 'NAT', 'EEM', 'IYR', 'KEY', 'OPEN', 'DM', 'TSLA', 'BXMT', 'T', 'TZA', 'BAC', 'MARA', 'UVXY', 'LOW', 'COST', 'HL', 'CHTR', 'TMF', 'ROKU', 'DOCU', 'PSEC', 'XHB', 'VMW', 'SABR', 'USB', 'DDOG', 'DB', 'V', 'NOW', 'XRT', 'SMCI', 'PFE', 'NYCB', 'BIDU', 'C', 'SPX', 'ETSY', 'EMB', 'SQQQ', 'CHPT', 'DASH', 'VZ', 'DNA', 'CL', 'ANET', 'WMT', 'MRO', 'WFC', 'MO', 'USO', 'ENVX', 'INTC', 'GEO', 'VFC', 'WE', 'MET', 'CHWY', 'PBR', 'KO', 'TH', 'QS', 'BTU', 'GLD', 'JD', 'XLY', 'KR', 'ASTS', 'WDC', 'HTZ', 'XLF', 'COP', 'PATH', 'SHEL', 'MXEF', 'SE', 'SPCE', 'UPS', 'RUN', 'DOW', 'ASHR', 'ONON', 'DAL', 'SPXL', 'SAVE', 'LUV', 'HD', 'JNJ', 'LYFT', 'UNH', 'BBY', 'CZR', 'NEE', 'STNG', 'SPXU', 'MMM', 'VNQ', 'IMGN', 'MSTR', 'AXP', 'TMO', 'XPO', 'FEZ', 'ENPH', 'AX', 'NVCR', 'GS', 'MRVL', 'ADM', 'GILD', 'IBB', 'FTCH', 'PARA', 'PINS', 'JBLU', 'SNY', 'BITO', 'PYPL', 'FAS', 'GME', 'LAZR', 'URNM', 'BX', 'MPW', 'UPRO', 'HPQ', 'AMZN', 'SAVA', 'TLT', 'ON', 'CAT', 'VLO', 'AR', 'IDXX', 'SWN', 'META', 'BABA', 'ZS', 'EWZ', 'ORCL', 'XOP', 'TJX', 'XP', 'EL', 'HAL', 'IEF', 'XLI', 'UPST', 'Z', 'TELL', 'LRCX', 'DLTR', 'BYND', 'PACW', 'CVNA', 'GSAT', 'CSCO', 'NU', 'KVUE', 'JPM', 'LCID', 'TLRY', 'AGNC', 'CGC', 'XLE', 'VOD', 'TEVA', 'JETS', 'UEC', 'FSR', 'ZIM', 'ABR', 'IQ', 'AMC', 'ALLY', 'HE', 'OKTA', 'ACN', 'MU', 'FLEX', 'SHOP', 'PLTR', 'CLX', 'LUMN', 'WHR', 'PAGP', 'IWM', 'WPM', 'TTWO', 'AI', 'ALGN', 'SPOT', 'BTG', 'IONQ', 'GE', 'DG', 'AMAT', 'XSP', 'PG', 'LULU', 'DE', 'MDT', 'RCL']
        self.scalar_tickers = ['SPX', 'VIX', 'OSTK', 'XSP', 'NDX', 'MXEF']
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.semaphore = asyncio.Semaphore(10)
        self.yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.thirty_days_from_now = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        self.fifteen_days_ago = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')
        self.fifteen_days_from_now = (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d')
        self.eight_days_from_now = (datetime.now() + timedelta(days=8)).strftime('%Y-%m-%d')
        self.eight_days_ago = (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d')
        self.timeframes = ['m1','m5', 'm10', 'm15', 'm20', 'm30', 'm60', 'm120', 'm240', 'd1']
        self.now_timestamp_int = int(datetime.now(timezone.utc).timestamp())
        self.day = int(86400)
        self.df = pd.read_csv('ticker_csv.csv')
        self.id = 15765933
        self.etf_list = pd.read_csv('etf_list.csv')
        #miscellaenous
                #sessions
        # Define the dictionary with all the rules
# Define the dictionary with all the rules
        self.rules_dict = {
            "boll": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish",
                    "wlas.screener.value.bullbear.bear"
                ],
                "term": [
                    "wlas.screener.value.term.long",
                    "wlas.screener.value.term.inter",
                    "wlas.screener.value.term.short"
                ]
            },
            "fsto": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish",
                    "wlas.screener.value.bullbear.bear"
                ],
                "term": [
                    "wlas.screener.value.term.long",
                    "wlas.screener.value.term.inter"
                ]
            },
            "macd": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish"
                ]
            },
            "rsitech": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish"
                ],
                "term": [
                    "wlas.screener.value.term.long"
                ]
            },
            "william": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish",
                    "wlas.screener.value.bullbear.bear"
                ],
                "term": [
                    "wlas.screener.value.term.long",
                    "wlas.screener.value.term.short",
                    "wlas.screener.value.term.inter"
                ]
            },
            "cci": {
                "term": [
                    "wlas.screener.value.term.inter",
                    "wlas.screener.value.term.short",
                    "wlas.screener.value.term.long"
                ],
                "bullbear": [
                    "wlas.screener.value.bullbear.bear",
                    "wlas.screener.value.bullbear.bullish"
                ]
            },
            "kst": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish",
                    "wlas.screener.value.bullbear.bear"
                ],
                "term": [
                    "wlas.screener.value.term.long",
                    "wlas.screener.value.term.short",
                    "wlas.screener.value.term.inter"
                ]
            },
            "mom": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish",
                    "wlas.screener.value.bullbear.bear"
                ],
                "term": [
                    "wlas.screener.value.term.long",
                    "wlas.screener.value.term.inter",
                    "wlas.screener.value.term.short"
                ]
            },
            "slowstach": {
                "bullbear": [
                    "wlas.screener.value.bullbear.bullish",
                    "wlas.screener.value.bullbear.bear"
                ],
                "term": [
                    "wlas.screener.value.term.long",
                    "wlas.screener.value.term.short",
                    "wlas.screener.value.term.inter"
                ]
            }
        }
        self.candle_patterns = ['gravestone', 'insidebar', 'outsidebar', 'gud', 'tbr', 'ibt', 'hhm', 'eb']
        self.indicators = ['mom', 'slowstach', 'kst', 'cci', 'william', 'rsi', 'macd', 'boll', 'fsto']
        self.ticker_df = pd.read_csv('ticker_csv.csv')
        self.ticker_to_id_map = dict(zip(self.ticker_df['ticker'], self.ticker_df['id']))
    def is_etf(self, symbol):
        """Check if a symbol is an ETF."""
        return symbol in self.etf_list['Symbol'].values
    async def fetch_endpoint(self, headers, endpoint):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(endpoint) as resp:
                return await resp.json()


    async def get_webull_id(self, symbol):
        """Converts ticker name to ticker ID to be passed to other API endpoints from Webull."""
        ticker_id = self.ticker_to_id_map.get(symbol)
        return ticker_id

    async def multi_quote(self, tickers=['AAPL', 'SPY']):
        """Query multiple tickers using the Webull API"""


        tasks = [self.get_webull_id(str(ticker)) for ticker in tickers]
        
        ticker_ids = await asyncio.gather(*tasks)


        ticker_ids = ','.join(str(ticker_id) for ticker_id in ticker_ids)
        print(ticker_ids)
        endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids={ticker_ids}&includeSecu=1&delay=0&more=1"

        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint)
            data = response.json()


            multi_quote = MultiQuote(data)

            return multi_quote
        
    async def candle_pattern_screener(self, headers, candle_pattern):
        """
        
        Candle types:
        
        
        >>> ihss - inverted hammer
        >>> gravestone
        >>> insidebar
        >>> outsidebar
        >>> gud - gap up or down
        >>> tbr - two bar reversal
        >>> ibt - island bottom/top
        >>> hhm - hammer / hanging man
        >>> eb - exhaustion bar
        """
        url = "https://quotes-gw.webullfintech.com/api/wlas/screener/ng/query"

        payload = {"fetch":200,"rules":{"wlas.screener.rule.region":"securities.region.name.6","wlas.screener.group.technical.signals":None,f"wlas.screener.rule.{candle_pattern}":"{\"wlas.screener.value.bullbear\":[\"wlas.screener.value.bullbear.bullish\",\"wlas.screener.value.bullbear.bear\"],\"wlas.screener.value.term\":[\"wlas.screener.value.term.long\",\"wlas.screener.value.term.inter\",\"wlas.screener.value.term.short\"]}"},"sort":{"rule":"wlas.screener.rule.volume","desc":True},"attach":{"hkexPrivilege":False}}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                response_data = await response.json()

                items = response_data.get('items')

                symbols = [i.get('symbol') for i in items]

                return symbols
            

    async def technical_screener(self, headers, technical_indicator, sentiment, time_horizon):
        """indicator types:
        >>> mom - momentum
        >>> slowstach
        >>> kst
        >>> cci
        >>> william
        >>> rsi
        >>> macd
        >>> fsto
        >>> boll

        sentiment:
        >>> bullish
        >>> bear

        time horizons:
        >>> long
        >>> short
        >>> inter (medium)

        """
        url = "https://quotes-gw.webullfintech.com/api/wlas/screener/ng/query"
        payload = {
            "fetch": 200,
            "rules": {
                "wlas.screener.rule.region": "securities.region.name.6",
                "wlas.screener.group.technical.signals": None,
                f"wlas.screener.rule.{technical_indicator}": f"""{{
                    "wlas.screener.value.bullbear": ["wlas.screener.value.bullbear.{sentiment}"],
                    "wlas.screener.value.term": ["wlas.screener.value.term.{time_horizon}"]
                }}"""
            },
            "sort": {
                "rule": "wlas.screener.rule.price",
                "desc": True
            },
            "attach": {
                "hkexPrivilege": False
            }
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, headers=headers) as response:
                    response_data = await response.json()


                    items = response_data.get('items')
                    ticker = [i.get('ticker') for i in items]
                    symbols = [i.get('symbol') for i in ticker]
                    volume = [float(i.get('volume')) for i in ticker]


                    dict = { 
                        'sym': symbols,
                    }

                    df = pd.DataFrame(dict)
                    df['indicator'] = technical_indicator
                    df['sentiment'] = sentiment
                    df['timeframe'] = time_horizon
                    return df
            except Exception as e:
                return f"No results for {technical_indicator} on the {time_horizon} {sentiment}"

            

    async def run_screeners_for_signal(self, headers, technical_signal):
        results = []
        rule_values = self.rules_dict[technical_signal]
        bullbear_values = rule_values.get("bullbear", ["wlas.screener.value.bullbear.bullish", "wlas.screener.value.bullbear.bear"])
        term_values = rule_values.get("term", ["wlas.screener.value.term.long", "wlas.screener.value.term.inter", "wlas.screener.value.term.short"])

        for bullbear in bullbear_values:
            for term in term_values:
                result = await self.fetch_screened_data(headers, technical_signal, bullbear, term)
                results.append(result)
        
        # Concat all results into a final DataFrame
        final_df = pd.DataFrame(results)
        return final_df
    async def get_bars(self, headers, ticker:str, interval:str='m1', count:str='100'):
        "Get candle bars for a ticekr."
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPXW'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            
            tickerid = await self.get_webull_id(ticker)

            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())

            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query-mini?tickerId={tickerid}&type={interval}&count={count}&restorationType=1&loadFactor=1&extendTrading=1'

            interval_mapping = {
                'm1': '1 min',
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            timespan = interval_mapping.get(interval, 'minute')

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(base_fintech_gw_url)
                r = data.json()
                if r and isinstance(r, list) and 'data' in r[0]:
                    data = r[0]['data']
                    if data is not None:
                        parsed_data = []
                        for entry in data:
                            values = entry.split(',')
                            if values[-1] == 'NULL':
                                values = values[:-1]
                            parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                        
                        sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                        
                        columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                        
                        df = pd.DataFrame(sorted_data, columns=columns)
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)
                        df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
                        df['Ticker'] = ticker
                        df['timespan'] = timespan
                        return df
        except Exception as e:
            print(e)
            
    # Detecting unfilled gaps in stock price data
    async def find_unfilled_gaps(self, ticker:str, interval:str):
        ticker = ticker.upper()
        unfilled_gaps=[]
        async for df in self.get_bars(ticker=ticker, interval=interval):

            df.sort_values(by='Timestamp', ascending=True, inplace=True)
            # Assuming the DataFrame is sorted in ascending order by 'Timestamp'
            for i in range(1, len(df)):
                previous_row = df.iloc[i - 1]
                current_row = df.iloc[i]
                
                # Checking for gap up
                if current_row['Low'] > previous_row['High']:
                    gap = {
                        'gap_date': current_row['Timestamp'],
                        'gap_range': (previous_row['High'], current_row['Low'])
                    }
                    # Check in the following days if the gap has been filled
                    filled = df[i+1:].apply(
                        lambda row: row['Low'] <= gap['gap_range'][1] and row['High'] >= gap['gap_range'][0], axis=1
                    ).any()
                    if not filled:
                        unfilled_gaps.append(gap)

                # Checking for gap down
                elif current_row['High'] < previous_row['Low']:
                    gap = {
                        'gap_date': current_row['Timestamp'],
                        'gap_range': (current_row['High'], previous_row['Low'])
                    }
                    # Check in the following days if the gap has been filled
                    filled = df[i+1:].apply(
                        lambda row: row['Low'] <= gap['gap_range'][1] and row['High'] >= gap['gap_range'][0], axis=1
                    ).any()
                    if not filled:
                        unfilled_gaps.append(gap)

            return unfilled_gaps
        

    async def deals(self, symbol:str, headers):
        try:
            tickerId = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/deals?count=50000&tickerId={tickerId}"

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(endpoint)
                data = data.json()

                data = data.get('data')

                data = Deals(data)
                return data
        except Exception as e:
            print(e)

    async def get_stock_quote(self, symbol:str):
        if symbol == 'SPX':
            symbol == 'SPXW'
        ticker_id = await self.get_webull_id(symbol)

        endpoint = f"https://quotes-gw.webullfintech.com/api/stock/tickerRealTime/getQuote?tickerId={ticker_id}&includeSecu=1&includeQuote=1&more=1"
        print(endpoint)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as resp:
                    r = await resp.json()

                    #data = WebullStockData(r)
                    try:

                        df = pd.DataFrame(r)
                        df = df.drop(columns=['secType', 'exchangeId', 'regionId', 'regionCode'])
                        return df
                    except Exception as e:
                        print(f"{e} | Attempting to use an index of 0...")
                        try:
                            df = pd.DataFrame(r, index=[0])
                            
                        except Exception as e:
                            print(f"Second attempt failed for {symbol}: {e}")
                        try:
                            df = df.drop(columns=['secType', 'exchangeId', 'regionId', 'regionCode'])
                            
                            return df
                        except Exception as e:
                            print(f'Giving up...{symbol}: {e}')
        except Exception as e:
            return f"Failed for {e}"


    async def get_analyst_ratings(self, symbol:str):
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint=f"https://quotes-gw.webullfintech.com/api/information/securities/analysis?tickerId={ticker_id}"
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()
                    data = Analysis(datas)
                    return data
        except Exception as e:
            print(e)
    

    async def get_short_interest(self, symbol:str):
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/information/brief/shortInterest?tickerId={ticker_id}"
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()
                    data = ShortInterest(datas)
                    return data
        except Exception as e:
            print(e)
    
    async def institutional_holding(self, symbol:str):
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/information/stock/getInstitutionalHolding?tickerId={ticker_id}"
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()
                    data = InstitutionStat(datas)
                    return data
        except Exception as e:
            print(e)
    

    async def volume_analysis(self, symbol:str):
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=10&tickerId={ticker_id}&type=0"
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()
                    data = WebullVolAnalysis(datas, symbol)
                    return data
        except Exception as e:
            print(e)
    

    async def new_cost_dist(self, symbol:str, start_date:str, end_date:str):
        """Returns list"""
        tickerId = await self.get_webull_id(symbol)
        try:
            endpoint = f"https://quotes-gw.webullfintech.com/api/quotes/chip/query?tickerId={tickerId}&startDate={start_date}&endDate={end_date}"
      
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    data = data.json()
                    data = data['data']
                    return NewCostDist(data,symbol)
        except Exception as e:
            print(e)


    async def cost_distribution(self, symbol:str, start_date:str=None, end_date:str=None):
        try:

            if start_date == None:
                start_date = self.thirty_days_ago
                

            if end_date == None:
                end_date = self.today

            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/quotes/chip/query?tickerId={ticker_id}&startDate={start_date}&endDate={end_date}"
            print(endpoint)
            datas = await self.fetch_endpoint(endpoint)
            data = CostDistribution(datas, symbol)
            return data
        except Exception as e:
            print(e)
        

    async def stock_quote(self, symbol:str):
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/bgw/quote/realtime?ids={ticker_id}&includeSecu=1&delay=0&more=1"
            datas = await self.fetch_endpoint(endpoint)
            data = WebullStockData(datas)
            return data
        except Exception as e:
            print(e)

    async def financials(self, symbol:str, financials_type:str='balancesheet'):
        """Argument
        
        Symbol: the symbol to query
        """
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/{financials_type}?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit=4"
        
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()

                data = datas['data'] if 'data' in datas else None
                if data is not None and financials_type == 'incomestatement':
                    data = FinancialStatement(datas).df.to_dict('records')
                    return data
                if data is not None and financials_type == 'balancesheet':
                    data = BalanceSheet(datas).df.to_dict('records')
                    return data
                if data is not None and financials_type == 'cashflow':
                    data = CashFlow(datas).df.to_dict('records')
                    return data
        except Exception as e:
            print(e)
    


    async def quote(self, ticker):
        tickerid = await self.get_webull_id(ticker)

        url = f"https://quotes-gw.webullfintech.com/api/stock/tickerRealTime/getQuote?tickerId={tickerid}&includeSecu=1&includeQuote=1&more=1"

        async with httpx.AsyncClient() as client:
            dict = {}
            data = await client.get(url)
            if data.status_code == 200:
                data = data.json()
                if not self.is_etf(ticker):
                    forwardPe = float(data.get('forwardPe',0))
                    indicatedPe = float(data.get('indicatedPe',0))
                    peTTM = float(data.get('peTtm'))
                    eps = float(data.get('eps', 0))
                    epsTTM = float(data.get('epsTtm', 0))
                    price_to_book = float(data.get('pb', 0))
                    dict['forward_pe'] = forwardPe
                    dict['indicated_pe'] = indicatedPe
                    dict['pe_ttm'] = peTTM
                    dict['eps'] = eps
                    dict['eps_ttm'] = epsTTM
                    dict['price_to_book'] = price_to_book
                    
                underlying_open = float(data.get('open'))
                underlying_close = float(data.get('close'))
                underlying_high = float(data.get('high'))
                underlying_low = float(data.get('low'))
                underlying_change_pct = round(float(data.get('changeRatio')))
                underlying_volume = float(data.get('volume'))
                vibrateRatio = float(data.get('vibrateRatio'))
                avgVol10D = float(data.get('avgVol10D'))
                avgVol3M = float(data.get('avgVol3M'))


                dict['underlying_close'] = underlying_close
                dict['underlying_open'] = underlying_open
                dict['underlying_high'] = underlying_high
                dict['underlying_low'] = underlying_low
                dict['underlying_change_pct'] = underlying_change_pct
                dict['underlying_volume'] = underlying_volume
                dict['vibrate_ratio'] = vibrateRatio
                dict['avg_vol_10d'] = avgVol10D
                dict['avg_vol_3m'] = avgVol3M


                return dict



    async def news(self, symbol:str, pageSize:str='100', headers=None):
        if headers == None:
            raise ValueError("DataFrame does not contain required columns: 'iv', 'expiry', 'strike'")
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://nacomm.webullfintech.com/api/information/news/tickerNews?tickerId={ticker_id}&currentNewsId=0&pageSize={pageSize}"
            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()
                    data = NewsItem(datas)
                    return data
        except Exception as e:
            print(e)
    

    async def company_brief(self, symbol:str, as_dataframe:bool=False):
        """
        RETURNS THREE THINGS

        >>> companyBrief_df
        >>> executives_df
        >>> sectors_df
        """
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint=f"https://quotes-gw.webullfintech.com/api/information/stock/brief?tickerId={ticker_id}"    
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()


                companyBrief = CompanyBrief(datas['companyBrief'])
                sectors = Sectors(datas['sectors'])
                executives = Executives(datas['executives'])

                # Convert to DataFrames
                companyBrief_df = companyBrief.as_dataframe
                sectors_df = sectors.as_dataframe
                executives_df = executives.as_dataframe

                
                return companyBrief, sectors, executives
        except Exception as e:
            print(e)

    async def balance_sheet(self, symbol:str, limit:str='11'):
        ticker_id = await self.get_webull_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/balancesheet?tickerId={ticker_id}&type=101&fiscalPeriod=0&limit={limit}"
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint)
            if data.status_code == 200:
                datas = data.json()
                data = BalanceSheet(datas)
                return data
    
    async def cash_flow(self, symbol:str, limit:str='12'):
        ticker_id = await self.get_webull_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/cashflow?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit={limit}"
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint)
            if data.status_code == 200:
                datas = data.json()
                data = CashFlow(datas)
                return data
    
    async def income_statement(self, symbol:str, limit:str='12'):
        ticker_id = await self.get_webull_id(symbol)
        endpoint = f"https://quotes-gw.webullfintech.com/api/information/financial/incomestatement?tickerId={ticker_id}&type=102&fiscalPeriod=1,2,3,4&limit={limit}"
        async with httpx.AsyncClient() as client:
            data = await client.get(endpoint)
            if data.status_code == 200:
                datas = data.json()
                data = FinancialStatement(datas)
                return data
    

    async def order_flow(self, headers, symbol:str, type:str='0', count:str='1', ):
        """
        Gets order flow for tickers
        """
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count={count}&tickerId={ticker_id}&type={type}"

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(endpoint)
                data = data.json()
                return OrderFlow(data)
        except Exception as e:
            print(e)
        

    async def price_streamer(self, symbol:str, type:str='0'):
        """
        Type:
        >>> 0 = today
        >>> 1 = yesterday
        """
        ticker_id = await self.get_webull_id(symbol)
        url=f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/stat?count=50000&tickerId={ticker_id}&type={type}"
        async with httpx.AsyncClient() as client:
            data = await client.get(url)
            data = data.json()

            return PriceStreamer(data)


    async def capital_flow(self, symbol:str):
        """RETURNS A TUPLE OBJECT"""
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/capitalflow/ticker?tickerId={ticker_id}&showHis=true"
            
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()

                latest = datas['latest']
                historic = datas['historical']
                date = [i.get('date') for i in historic]
                historic_items = [i.get('item') for i in historic]
                item = latest['item']

                print(item)
                data = CapitalFlow(item, symbol)
                historic = CapitalFlowHistory(historic_items, date)
            
                return data, historic
        except Exception as e:
            print(e)
        

    async def etf_holdings(self, symbol:str, pageSize:str='200'):
        try:
            ticker_id = await self.get_webull_id(symbol)
            endpoint = f"https://quotes-gw.webullfintech.com/api/information/company/queryEtfList?tickerId={ticker_id}&pageIndex=1&pageSize={pageSize}"
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                if data.status_code == 200:
                    datas = data.json()

                    data = ETFHoldings(datas)
                    return data
        except Exception as e:
            print(e)
        

    
    async def get_quote(self, ticker, headers):
        try:
            ticker_id = await self.get_webull_id(ticker)
            endpoint = f"https://quotes-gw.webullfintech.com/api/stock/tickerRealTime/getQuote?tickerId={ticker_id}&includeSecu=1&includeQuote=1&more=1"
            async with httpx.AsyncClient() as client:
                data = await client.get(endpoint)
                data = data.json()
                # Updated data_dict


                # Extracting data from the input dictionary
                name = data.get('name', None)
                symbol = data.get('symbol', None)
                derivative_support = data.get('derivativeSupport', 0)
                close = float(data.get('close', 0))
                change = float(data.get('change', 0))
                change_ratio = round(float(data.get('changeRatio', 0)) * 100, 2)
                market_value = float(data.get('marketValue', 0))
                volume = float(data.get('volume', 0))
                turnover_rate = round(float(data.get('turnoverRate', 0)) * 100, 2)
                open = float(data.get('open', 0))
                high = float(data.get('high', 0))
                low = float(data.get('low', 0))
                vibrate_ratio = float(data.get('vibrateRatio', 0))
                avg_vol_10d = float(data.get('avgVol10D', 0))
                avg_vol_3m = float(data.get('avgVol3M', 0))
                neg_market_value = float(data.get('negMarketValue', 0))
                pe = float(data.get('pe', 0))
                forward_pe = float(data.get('forwardPe', 0))
                indicated_pe = float(data.get('indicatedPe', 0))
                pe_ttm = float(data.get('peTtm', 0))
                eps = float(data.get('eps', 0))
                eps_ttm = float(data.get('epsTtm', 0))
                pb = float(data.get('pb', 0))
                total_shares = float(data.get('totalShares', 0))
                outstanding_shares = float(data.get('outstandingShares', 0))
                fifty_two_wk_high = float(data.get('fiftyTwoWkHigh', 0))
                fifty_two_wk_low = float(data.get('fiftyTwoWkLow', 0))
                dividend = float(data.get('dividend', 0))
                yield_ = float(data.get('yield', 0))
                latest_dividend_date = data.get('latestDividendDate', None)
                latest_split_date = data.get('latestSplitDate', None)
                latest_earnings_date = data.get('latestEarningsDate', None)
                ps = float(data.get('ps', 0))
                bps = float(data.get('bps', 0))
                estimate_earnings_date = data.get('estimateEarningsDate', None)

                # Calculate percentage from 52-week high
                pct_from_52_high = ((fifty_two_wk_high - close) / fifty_two_wk_high) * 100 if fifty_two_wk_high != 0 else None
                pct_from_52_high = round(float(pct_from_52_high),2)
                # Calculate percentage from 52-week low
                pct_from_52_low = ((close - fifty_two_wk_low) / fifty_two_wk_low) * 100 if fifty_two_wk_low != 0 else None
                pct_from_52_low = round(float(pct_from_52_low),2)
                # Calculate volume vs average volume (10 days)
                volume_vs_avg_vol_10d = (volume / avg_vol_10d) if avg_vol_10d != 0 else None
                volume_vs_avg_vol_10d = round(float(volume_vs_avg_vol_10d)* 100, 2)
                # Calculate volume vs average volume (3 months)
                volume_vs_avg_vol_3m = (volume / avg_vol_3m) if avg_vol_3m != 0 else None
                volume_vs_avg_vol_3m = round(float(volume_vs_avg_vol_3m)* 100, 2)

                # Create new earnings metrics
                earnings_to_price = (eps_ttm / close) if close != 0 else None
                earnings_to_price = round(float(earnings_to_price)*100,2)
                forward_earnings_to_price = (forward_pe / close) if close != 0 else None
                forward_earnings_to_price = round(float(forward_earnings_to_price) * 100, 2)

                data_dict = {
                    'name': name,
                    'ticker': symbol,
                    'derivative_support': derivative_support,
                    'close': close,
                    'change': change,
                    'change_ratio': change_ratio,
                    'market_value': market_value,
                    'volume': volume,
                    'turnover_rate': turnover_rate,
                    'open': open,
                    'high': high,
                    'low': low,
                    'vibrate_ratio': vibrate_ratio,
                    'avg_vol_10d': avg_vol_10d,
                    'avg_vol_3m': avg_vol_3m,
                    'neg_market_value': neg_market_value,
                    'pe': pe,
                    'forward_pe': forward_pe,
                    'indicated_pe': indicated_pe,
                    'pe_ttm': pe_ttm,
                    'eps': eps,
                    'eps_ttm': eps_ttm,
                    'pb': pb,
                    'total_shares': total_shares,
                    'outstanding_shares': outstanding_shares,
                    'fifty_two_wk_high': fifty_two_wk_high,
                    'fifty_two_wk_low': fifty_two_wk_low,
                    'dividend': dividend,
                    'yield': yield_,
                    'latest_dividend_date': latest_dividend_date,
                    'latest_split_date': latest_split_date,
                    'latest_earnings_date': latest_earnings_date,
                    'ps': ps,
                    'bps': bps,
                    'estimate_earnings_date': estimate_earnings_date,
                    'pct_from_52_high': pct_from_52_high,
                    'pct_from_52_low': pct_from_52_low,
                    'volume_vs_avg_vol_10d': volume_vs_avg_vol_10d,
                    'volume_vs_avg_vol_3m': volume_vs_avg_vol_3m,
                    'earnings_to_price': earnings_to_price,
                    'forward_earnings_to_price': forward_earnings_to_price,

                }

                # Print to verify the updated dictionary
            
                df = pd.DataFrame(data_dict, index=[0])

                return df
        except Exception as e:
            print(e)
    async def async_get_td9(self, ticker, interval, headers):
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPXW'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            
            tickerid = await self.get_webull_id(ticker)

            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())

            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query?tickerIds={tickerid}&type={interval}&timestamp={timeStamp}&count=800&extendTrading=1'

            interval_mapping = {
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            timespan = interval_mapping.get(interval, 'minute')

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(base_fintech_gw_url)
                r = data.json()
                if r and isinstance(r, list) and 'data' in r[0]:
                    data = r[0]['data']
                    if data is not None:
                        parsed_data = []
                        for entry in data:
                            values = entry.split(',')
                            if values[-1] == 'NULL':
                                values = values[:-1]
                            parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                        
                        sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                        
                        columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                        
                        df = pd.DataFrame(sorted_data, columns=columns)
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)
                        df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
                        df['Ticker'] = ticker
                        df['timespan'] = timespan

                        td9_df = df.head(13)
                        print(td9_df)
                        return td9_df
        except Exception as e:
            print(e)

  
    async def ta_bollinger(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month

        ARGS:
        window: default 14
        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.async_get_td9(ticker, interval, headers=headers)
                
            boll_hband = ta.volatility.bollinger_hband(close=df['Close'], fillna=True)
            boll_lband = ta.volatility.bollinger_lband(close=df['Close'], fillna=True)
            boll_pband = ta.volatility.bollinger_pband(close=df['Close'], fillna=True)
            boll_wband = ta.volatility.bollinger_wband(close=df['Close'], fillna=True)
            boll_mavg = ta.volatility.bollinger_mavg(close=df['Close'])
        

            df['boll_wband'] = boll_wband
            df['boll_hband'] = boll_hband
            df['boll_lband'] = boll_lband
            df['boll_pband'] = boll_pband
            df['boll_mavg'] = boll_mavg

            
            return df
        except Exception as e:
            print(e)


    async def ta_donchain(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.async_get_td9(ticker, interval, headers=headers)
                
            donchain_hband = ta.volatility.donchian_channel_hband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            donchain_lband = ta.volatility.donchian_channel_lband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            donchain_pband=ta.volatility.donchian_channel_pband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            donchain_mband = ta.volatility.donchian_channel_mband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            donchain_wband = ta.volatility.donchian_channel_wband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)

            df['donchain_hband'] = donchain_hband
            df['donchain_lband'] = donchain_lband
            df['donchain_midband'] = donchain_mband
            df['donchain_pctband'] = donchain_pband
            df['donchain_wband'] = donchain_wband
            
            return df
        except Exception as e:
            print(e)

    async def ta_kelter_channel(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)


            kelter_hband = ta.volatility.keltner_channel_hband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            kelter_lband = ta.volatility.keltner_channel_lband(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            kelter_mavg = ta.volatility.keltner_channel_mband(high=df['High'], close=df['Close'], low=df['Low'], fillna=True)
            kelter_pband = ta.volatility.keltner_channel_pband(high=df['High'], close=df['Close'], low=df['Low'], fillna=True)
            kelter_wband = ta.volatility.keltner_channel_wband(high=df['High'], close=df['Close'], low=df['Low'], fillna=True)


            df['kelter_hband'] = kelter_hband
            df['kelter_lband'] = kelter_lband
            df['kelter_mavg'] = kelter_mavg
            df['kelter_pctband'] = kelter_pband
            df['kelter_wband'] = kelter_wband

            
            return df
        except Exception as e:
            print(e)


    async def ta_awesome_oscillator(self, ticker: str, interval: str, headers):
        """Gets a dataframe of the ease_of_movement indicator. 
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month


        """
        try:
            # Get the main dataframe (e.g., price data)
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)


            awesome_oscillator = ta.momentum.awesome_oscillator(high=df['High'], low=df['Low'], fillna=True)

            df['awesome_oscillator'] = awesome_oscillator

            
            return df
        except Exception as e:
            print(e)



    async def ta_kama(self, headers, ticker:str, interval:str='m60'):
        """Moving average designed to account for market noise or volatility. KAMA will closely follow prices when the price swings are relatively small and the noise is low. KAMA will adjust when the price swings widen and follow prices from a greater distance. This trend-following indicator can be used to identify the overall trend, time turning points and filter price movements.
        
        
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            

            kama = ta.momentum.kama(close=df['Close'], fillna=True)


            df['kama'] = kama


            return df
        except Exception as e:
            print(e)


    async def ta_ppo(self, headers, ticker:str, interval:str='m60'):
        """The Percentage Price Oscillator (PPO) is a momentum oscillator that measures the difference between two moving averages as a percentage of the larger moving average.

        https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo
                
        
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            

            ppo = ta.momentum.ppo(df['Close'], fillna=True)

            ppo_hist = ta.momentum.ppo_hist(df['Close'], fillna=True)

            ppo_signal = ta.momentum.ppo_signal(df['Close'], fillna=True)


            df['ppo'] = ppo
            df['ppo_hist'] = ppo_hist
            df['ppo_signal'] = ppo_signal

            return df
        except Exception as e:
            print(e)


    async def ta_stoch(self, headers, ticker:str, interval:str='m60'):
        """Developed in the late 1950s by George Lane. The stochastic oscillator presents the location of the closing price of a stock in relation to the high and low range of the price of a stock over a period of time, typically a 14-day period.

        https://www.investopedia.com/terms/s/stochasticoscillator.asp
                        
                
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            

            stoch = ta.momentum.stoch(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            stoch_signal = ta.momentum.stoch_signal(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)

            df['stoch'] = stoch
            df['stoch_signal'] = stoch_signal



            return df
        except Exception as e:
            print(e)


    async def ta_tsi(self, headers, ticker:str, interval:str='m60'):
        """Shows both trend direction and overbought/oversold conditions.

        https://en.wikipedia.org/wiki/True_strength_index
                                
                
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            

            tsi = ta.momentum.tsi(close=df['Close'], fillna=True)

            df['tsi'] = tsi

            return df
        except Exception as e:
            print(e)

    async def ta_williamsr(self, headers, ticker:str, interval:str='m60'):
        """Developed by Larry Williams, Williams %R is a momentum indicator that is the inverse of the Fast Stochastic Oscillator. Also referred to as %R, Williams %R reflects the level of the close relative to the highest high for the look-back period. In contrast, the Stochastic Oscillator reflects the level of the close relative to the lowest low. %R corrects for the inversion by multiplying the raw value by -100. As a result, the Fast Stochastic Oscillator and Williams %R produce the exact same lines, only the scaling is different. Williams %R oscillates from 0 to -100.

        Readings from 0 to -20 are considered overbought. Readings from -80 to -100 are considered oversold.

        Unsurprisingly, signals derived from the Stochastic Oscillator are also applicable to Williams %R.

        %R = (Highest High - Close)/(Highest High - Lowest Low) * -100

        Lowest Low = lowest low for the look-back period Highest High = highest high for the look-back period %R is multiplied by -100 correct the inversion and move the decimal.

        From: https://www.investopedia.com/terms/w/williamsr.asp The Williams %R oscillates from 0 to -100. When the indicator produces readings from 0 to -20, this indicates overbought market conditions. When readings are -80 to -100, it indicates oversold market conditions.
                                        
                
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            

            williams_r = ta.momentum.williams_r(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)

            df['williams_r'] = williams_r

            return df
        except Exception as e:
            print(e)


    async def ta_williamsr(self, headers, ticker:str, interval:str='m60'):
        """
        
        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            
            macd= ta.trend.macd(close=df['close'], fillna=True)
            macd_diff = ta.trend.macd_diff(close=df['Close'], fillna=True)
            macd_signal = ta.trend.macd_signal(close=df['Close'], fillna=True)


            df['macd'] = macd
            df['macd_diff'] = macd_diff
            df['macd_signal'] = macd_signal

            return df
        except Exception as e:
            print(e)




    async def ta_vortex(self, headers, ticker:str, interval:str='m60'):
        """
        It consists of two oscillators that capture positive and negative trend movement. A bearish signal triggers when the negative trend indicator crosses above the positive trend indicator or a key level.


        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            
            vortex_neg = ta.trend.vortex_indicator_neg(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            vortex_pos = ta.trend.vortex_indicator_pos(high=df['High'], low=df['Low'], close=df['Close'], fillna=True)
            df['vortex_pos'] = vortex_pos
            df['vortex_neg'] = vortex_neg
            return df
        except Exception as e:
            print(e)


    async def ta_cumulative_return(self, headers, ticker:str, interval:str='m60'):
        """

        INTERVALS:
        >>> m1 - 1 minute
        >>> m5 - 5 minute
        >>> m30 - 30 minute
        >>> m60 - 1 hour
        >>> m120 - 2 hour
        >>> m240 - 4 hour
        >>> d - day
        >>> w - week
        >>> m - month
        """
        try:
            df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)
            
            cum = ta.others.cumulative_return(close=df['Close'])

            df['cum_return'] = cum
            return df
        except Exception as e:
            print(e)
