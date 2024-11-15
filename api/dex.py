import asyncio
import websockets
import telebot
from telebot import formatting
import json
from datetime import datetime
import time
import os


Api = os.environ["API"]
ID = "-1001873201570"

headers =  {
    "Host": "io.dexscreener.com",
    "Connection": "Upgrade",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "User-Agent": "Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Upgrade": "websocket",
    "Origin": "https://dexscreener.com",
    "Sec-WebSocket-Version": "13",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en-IN;q=0.9,en;q=0.8",
    "Sec-WebSocket-Key": "QvmwsgXQoeeZLZd45uUdQw==",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"
  }

class DexBot():
  def __init__(self, api_key, channel_id, chain=False, max_token=10):
    self.api_key = api_key
    self.channel_id = channel_id
    self.bot = telebot.TeleBot(api_key)
    self.addr = os.environ['ADDRESS']
    self.chain = chain
    self.max_token = max_token

  async def connect(self):
    async with websockets.connect(self.addr, additional_headers=headers) as websocket:
        message = "hi"
        await websocket.send(message)
        response = await websocket.recv()
        print(response)
        self.bot.send_message(self.channel_id, response, parse_mode='MarkdownV2', disable_web_page_preview=True)
        return json.loads(response)
      
  def tg_send(self, message):
    try:
        self.bot.send_message(self.channel_id, message, parse_mode='MarkdownV2', disable_web_page_preview=True)
    except Exception as e:
        print(e)

  def token_getter(self):
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(self.connect())
    # print(response)
    tokens = response["pairs"][:10][::-1] # flipped the list
    data = ""
    numbers = ["🔟", "9️⃣", "8️⃣", "7️⃣", "6️⃣", "5️⃣", "4️⃣", "3️⃣", "2️⃣", "1️⃣"]
    num = 0

    for i, token in enumerate(tokens):
        if num == self.max_token:
            break

        if self.chain is False or self.chain.lower() in token["chainId"]:
            prices = ""
            url = f'https://dexscreener.com/{token.get("chainId", "-")}/{token.get("pairAddress", "-")}'
            name = formatting.escape_markdown(token['baseToken']['symbol']) if 'baseToken' in token else "-"
            price_usd = formatting.escape_markdown(token.get('priceUsd', "-"))
            volume = int(token['volume'].get('h24', "-")) if 'h24' in token["volume"] else "-"
            market_cap = int(token.get('marketCap', "-"))
            liquidity_usd = int(token['liquidity'].get('usd', "-")) if 'liquidity' in token else "-"
            pair_created_at = token.get('pairCreatedAt', "-")
            holders_h24 = int(token['makers'].get('h24', "-")) if 'makers' in token else "-"
            price_change = [token["priceChange"].get('m5', 0), token["priceChange"].get('h1', 0), token["priceChange"].get('h6', 0), token["priceChange"].get('h24', 0)]
            time_difference = datetime.fromtimestamp(pair_created_at / 1000) - datetime.now()
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
                price_value = int(price)
                if price_value >= 0 and price_value < 45:
                    price = f"💹 {price_value:,}"
                elif price_value > 45:
                    price = f"💸 {price_value:,}"
                elif price_value < 0 and price_value > -45:
                    price = f"🩸 {price_value:,}"
                elif price_value < -45:
                    price = f"💥 {price_value:,}"

                prices += f"{price}% "
                
            
            info = f"{numbers[num]} *Token Name:* [{name}/ {(token['chainId'])}]({url})\n```{name}\n💸 Price: {price_usd} \n💎 TMCap: {market_cap:,}$ \n💧 Liquidity: {liquidity_usd:,}$ \n📢 volume: {volume:,}$ \n📝 Holders: {holders_h24}\n📆 Pool created: {time_ago} \n🌡 {prices}```"

            data += f"{info}\n"
            num += 1
            #print(data)

    return data

