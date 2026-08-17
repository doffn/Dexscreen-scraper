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

nest_asyncio.apply()

Api = "TG bot API here"
ID = "Channel ID"


class DexBot():
    def __init__(self, api_key, url, channel_id=ID, max_token=10):
        self.api_key = api_key
        self.channel_id = channel_id
        self.max_token = max_token
        self.url = url

    def generate_sec_websocket_key(self):
        random_bytes = os.urandom(16)
        return base64.b64encode(random_bytes).decode('utf-8')

    def get_headers(self):
        return {
            "Host": "io.dexscreener.com",
            "Connection": "Upgrade",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "Upgrade": "websocket",
            "Origin": "https://dexscreener.com",
            "Sec-WebSocket-Version": "13",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-WebSocket-Key": self.generate_sec_websocket_key()
        }

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
                    results[address] = f"Error: Status code {response.status_code}"
            except requests.RequestException as e:
                # Handle request exceptions
                results[address] = f"Error making request: {str(e)}"

        # Extracting values as a list
        results = list(results.values())
        # Output the result as JSON

        return json.dumps({"data": results}, indent=2)

    async def connect(self):
        headers = self.get_headers()
        session = None
        ws = None

        try:
            session = AsyncSession(headers=headers)

            ws = await session.ws_connect(
                self.url,
                headers=headers
            )

            print("Connected:", self.url)

            while True:
                try:
                    data = await ws.recv()

                    if not data:
                        print("No data received.")
                        break

                    # recv() returns the actual message, not a list
                    if isinstance(data, bytes):
                        response = data.decode(
                            "utf-8",
                            errors="ignore"
                        )
                    else:
                        response = str(data)

                    print("Received:", len(response), "bytes")

                    if response:
                        return response

                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break

        except Exception as e:
            print(f"Connection error: {e}")
            return None

        finally:
            if ws:
                try:
                    await ws.close()
                except:
                    pass

            if session:
                try:
                    await session.close()
                except:
                    pass

    def tg_send(self, message):
        try:
            url = f"https://api.telegram.org/bot{self.api_key}/sendMessage"

            requests.post(
                url,
                json={
                    "chat_id": self.channel_id,
                    "text": message,
                    "disable_web_page_preview": True
                },
                timeout=10
            )

        except Exception as e:
            print(f"Telegram sending error: {e}")

    def start(self):
        # Run the async connection
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mes = loop.run_until_complete(self.connect())
        loop.close()

        # Decode message, replacing non-printable characters with space
        decoded_text = ''.join(chr(b) if 32 <= b <= 126 else ' ' for b in mes)

        # Split into long words
        words = [w for w in decoded_text.split() if len(w) >= 65]


        extracted_tokens = []

        for token in words:
            try:
                token_lower = token.lower()

                # Skip URLs
                if any(substr in token_lower for substr in ["https", "http", "//", ".com"]):
                    continue

                # ETH addresses
                if "0x" in token_lower:
                    eth_match = re.findall(r'0x[0-9a-fA-F]{40,}', token)
                    if eth_match:
                        extracted_tokens.append(eth_match[-1])
                        continue

                # Pump tokens
                if "pump" in token_lower:
                    pump_match = re.search(r'.{0,40}pump', token, re.IGNORECASE)
                    if pump_match:
                        extracted_tokens.append(pump_match.group(0).lstrip('V'))
                        continue

                # Bonk tokens
                if "bonk" in token_lower:
                    bonk_match = re.search(r'.{0,40}bonk', token, re.IGNORECASE)
                    if bonk_match.startswith('V'):
                        bonk_match = sol_token[1:]
                    if bonk_match:
                        extracted_tokens.append(bonk_match.group(0))
                        continue

                # Solana-like addresses (last 44 chars)
                sol_token = token[-44:]
                if sol_token.startswith('V'):
                    sol_token = sol_token[1:]
                extracted_tokens.append(sol_token)

            except Exception as e:
                print(f"Error processing token '{token}': {e}")


        print("Extraction complete")
        return extracted_tokens[:70]

    def token_getter(self, message):
        pass
