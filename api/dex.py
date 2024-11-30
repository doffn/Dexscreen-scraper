import asyncio
import base64
import os
from curl_cffi.requests import AsyncSession
import json
import nest_asyncio
import telebot
from telebot import formatting
from datetime import datetime
import time

# Apply nest_asyncio
nest_asyncio.apply()

Api = os.environ["API"]
ID = "-1001873201570"

class DexBot():
    def __init__(self, api_key, channel_id, chain=False, max_token=10):
        self.api_key = api_key
        self.channel_id = channel_id
        self.bot = telebot.TeleBot(api_key)
        self.addr = os.environ['ADDRESS']
        self.chain = chain
        self.max_token = max_token
        self.url = "wss://io.dexscreener.com/dex/screener/v4/pairs/h1/1?rankBy[key]=trendingScoreH6&rankBy[order]=desc"

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

    async def connect(self):
        headers = self.get_headers()
        try:
            session = AsyncSession(headers=headers)
            ws = await session.ws_connect(self.url)

            try:
                data = await ws.arecv()
                return json.loads(data[0])
            except Exception as e:
                print(f"Error receiving message: {str(e)}")
                return None
            finally:
                try:
                    await ws.close()
                except:
                    pass
                try:
                    await session.close()
                except:
                    pass
        except Exception as e:
            print(f"Connection error: {str(e)}")
            return None

    def tg_send(self, message):
        try:
            self.bot.send_message(self.channel_id, message, parse_mode='MarkdownV2', disable_web_page_preview=True)
        except Exception as e:
            print(e)

    def token_getter(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self.connect())
        loop.close()
        
        if not response or "pairs" not in response:
            return "Error fetching data"
            
        tokens = response["pairs"][:10][::-1]
        data = ""
        numbers = ["🔟", "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣"]
        num = 0

        for token in tokens:
            if num == self.max_token:
                break

            if self.chain is False or self.chain.lower() in token["chainId"].lower():
                prices = ""
                url = f'https://dexscreener.com/{token.get("chainId", "-")}/{token.get("pairAddress", "-")}'
                name = formatting.escape_markdown(token['baseToken']['symbol']) if 'baseToken' in token else "-"
                price_usd = formatting.escape_markdown(str(token.get('priceUsd', "-")))
                volume = int(float(token['volume'].get('h24', "0"))) if 'volume' in token and 'h24' in token['volume'] else 0
                market_cap = int(float(token.get('marketCap', "0")))
                liquidity_usd = int(float(token['liquidity'].get('usd', "0"))) if 'liquidity' in token else 0
                pair_created_at = int(token.get('pairCreatedAt', "0"))
                holders_h24 = int(token['makers'].get('h24', "0")) if 'makers' in token else 0
                
                price_change = [
                    token["priceChange"].get('m5', 0),
                    token["priceChange"].get('h1', 0),
                    token["priceChange"].get('h6', 0),
                    token["priceChange"].get('h24', 0)
                ]

                time_difference = datetime.now() - datetime.fromtimestamp(pair_created_at / 1000)
                days = time_difference.days
                hours = time_difference.seconds // 3600
                minutes = (time_difference.seconds % 3600) // 60

                if days > 0:
                    time_ago = f"{days}d {hours}h ago"
                elif hours > 0:
                    time_ago = f"{hours}h {minutes}m ago"
                else:
                    time_ago = f"{minutes}m ago"

                for price in price_change[::-1]:
                    price_value = float(price)
                    if price_value >= 0 and price_value < 45:
                        price = f"💹 {price_value:,.2f}"
                    elif price_value > 45:
                        price = f"💸 {price_value:,.2f}"
                    elif price_value < 0 and price_value > -45:
                        price = f"🩸 {price_value:,.2f}"
                    elif price_value < -45:
                        price = f"💥 {price_value:,.2f}"

                    prices += f"{price}% "

                info = f"{numbers[num]} *Token Name:* [{name}/ {(token['chainId'])}]({url})\n```{name}\n💸 Price: {price_usd} \n💎 TMCap: {market_cap:,}$ \n💧 Liquidity: {liquidity_usd:,}$ \n📢 volume: {volume:,}$ \n📝 Holders: {holders_h24}\n📆 Pool created: {time_ago} \n🌡 {prices}```"

                data += f"{info}\n"
                num += 1

        return data