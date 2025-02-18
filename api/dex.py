import asyncio
import base64
import os
from curl_cffi.requests import AsyncSession
import json
import nest_asyncio
from datetime import datetime
import time
import struct
from decimal import Decimal, ROUND_DOWN
import re
import requests

# Apply nest_asyncio
nest_asyncio.apply()

Api = os.environ["API"]  
ID = "-1001873201570"

class DexBot():
    def __init__(self, api_key, channel_id=1234, chain=False, max_token=10):
        self.api_key = api_key
        self.channel_id = channel_id
        self.chain = chain
        self.max_token = max_token
        self.url = "wss://io.dexscreener.com/dex/screener/v4/pairs/h24/1?rankBy[key]=trendingScoreH6&rankBy[order]=desc"

    def generate_sec_websocket_key(self):
        random_bytes = os.urandom(16)
        key = base64.b64encode(random_bytes).decode('utf-8')
        return key

    def get_headers(self):
        headers = {
            "Host": "io.dexscreener.com",
            "Connection": "Upgrade",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Upgrade": "websocket",
            "Origin": "https://dexscreener.com",
            'Sec-WebSocket-Version': '13',
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-WebSocket-Key": self.generate_sec_websocket_key()
        }
        return headers

    def format_token_data(self):

        """
        Fetch information about specific tokens from the Dexscreener API.

        Args:
            token_addresses (list): List of token addresses.

        Returns:
            dict: A dictionary containing data for each token address or an error message.
        """

        token_addresses = self.start()

        base_url = "https://api.dexscreener.com/latest/dex/tokens/"
        results = {}

        for address in token_addresses:
            try:
                # Make an API call for each token address
                response = requests.get(f"{base_url}{address}")
                if response.status_code == 200:
                    data = response.json()
                    # Store the relevant data for the token address
                    pairs = data.get('pairs', [])  # 'pairs' contains token market data
                    
                    if pairs and len(pairs) > 0:
                        results[address] = pairs[0]  # Store first pair's data
                    else:
                        results[address] = {"pairAddress": address,
                                            "Error": "No data Retrieved"}
                else:
                    # Handle HTTP errors
                    results[address] = f"Error: Status code {response.status_code}, {response.text}"
            except requests.RequestException as e:
                # Handle request exceptions
                results[address] = f"Error making request: {str(e)}"

        # Extracting values as a list
        results = list(results.values())
        # Output the result as JSON

        return json.dumps({"data": results}, indent=2)
      

    async def connect(self):
        headers = self.get_headers()
        try:
            session = AsyncSession(headers=headers)
            ws = await session.ws_connect(self.url)

            # Loop to keep receiving data until the connection is closed
            while True:
                try:
                    # Receive data from WebSocket
                    data = await ws.arecv()

                    if data:
                        response = data[0]  # Assuming the first element contains the desired message
                        # Process and return the data or handle it as needed
                        #print(response)  # You can replace this with your desired processing logic
                        if "pairs" in str(response):
                          return response

                    else:
                        # If no data is received, break out of the loop
                        print("No data received.")
                        break

                except Exception as e:
                    print(f"Error receiving message: {str(e)}")
                    break

            # Closing the WebSocket and session after the loop ends
            await ws.close()
            await session.close()

        except Exception as e:
            print(f"Connection error: {str(e)}")
            return f"Connection error: {str(e)}"


    def tg_send(self, message):
        try:
            self.bot.send_message(self.channel_id, message, parse_mode='MarkdownV2', disable_web_page_preview=True)
        except Exception as e:
            print(f"Telegram sending error: {e}")

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mes = loop.run_until_complete(self.connect())
        loop.close()

        # Find data between start and end markers
        start_marker = b'\x0c'  # Define start marker
        end_marker = b'\x02'    # Define end marker

        # Split the data by start_marker and end_marker and extract data between them
        extracted_data = []
        for chunk in mes.split(start_marker)[1:]:
            data_segment = chunk.split(end_marker)[0]

            if len(data_segment) > 30 and "solana" in str(data_segment):
                data = str(data_segment[16:])
                #print(data)

                if "pump" in data:
                  # Decode the bytes into a string
                  # Regular expression to capture 43 characters before "pump" and "pump" itself
                  data = data[47:]
                  pattern = r".{0,40}pump"
                  data = re.findall(pattern, data)[0]

                else:
                  data = data[:91]
                  data = re.sub(r'[^a-zA-Z0-9\s]', '', data)
                  #print(data[-44:])
                  data = data[-44:]


                    
                extracted_data.append(data)
        #print(extracted_data)
        return extracted_data


    def token_getter(self, message):
        pass