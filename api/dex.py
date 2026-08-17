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

        token_addresses = self.start()

        base_url = "https://api.dexscreener.com/latest/dex/tokens/"
        results = {}

        for address in token_addresses:
            try:
                response = requests.get(
                    f"{base_url}{address}",
                    timeout=15
                )

                if response.status_code == 200:
                    data = response.json()
                    pairs = data.get('pairs', [])

                    if pairs:
                        results[address] = pairs[0]
                    else:
                        results[address] = {
                            "pairAddress": address,
                            "Error": "No data Retrieved"
                        }
                else:
                    results[address] = {
                        "pairAddress": address,
                        "Error": f"Status code {response.status_code}"
                    }

            except requests.RequestException as e:
                results[address] = {
                    "pairAddress": address,
                    "Error": str(e)
                }

        results = list(results.values())

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

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            mes = loop.run_until_complete(self.connect())
        finally:
            loop.close()

        if not mes:
            print("WebSocket returned nothing.")
            return []

        # Decode bytes if necessary
        if isinstance(mes, bytes):
            decoded_text = mes.decode(
                "utf-8",
                errors="ignore"
            )
        else:
            decoded_text = str(mes)

        print("Message received:")
        print(decoded_text[:500])

        # Find addresses directly instead of splitting into words
        extracted_tokens = []

        # ETH / EVM
        eth_matches = re.findall(
            r'0x[0-9a-fA-F]{40}',
            decoded_text
        )

        extracted_tokens.extend(eth_matches)

        # Solana / Pump addresses
        sol_matches = re.findall(
            r'\b[A-HJ-NP-Za-km-z1-9]{32,44}\b',
            decoded_text
        )

        for token in sol_matches:
            if token not in extracted_tokens:
                extracted_tokens.append(token)

        # Pump addresses
        pump_matches = re.findall(
            r'\b[A-HJ-NP-Za-km-z1-9]{20,44}pump\b',
            decoded_text,
            re.IGNORECASE
        )

        for token in pump_matches:
            if token not in extracted_tokens:
                extracted_tokens.append(token)

        # Remove duplicates
        extracted_tokens = list(dict.fromkeys(extracted_tokens))

        print("Extraction complete")
        print("Tokens found:", extracted_tokens)

        return extracted_tokens[:self.max_token]

    def token_getter(self, message):
        pass

