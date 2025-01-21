from flask import Flask, request
from api.dex import *
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return """
        <body style="background-color:black; color:white; font-family: Arial, sans-serif;">
            <h1>Hello User! 👋</h1>
            <p>This will scrape from Dexscreener trending tokens by running the <a href="/dex" style="color: white; text-decoration: underline;">/dex</a> path.</p>
            <ol>
                <li>You need to add a bot inside a group. 🤖</li>
                <li>You need to get the channel ID. 📨</li>
                <li>You need to get the WebSocket URL for the filters for the Dexscreener. Use this format:
                    <pre style="background-color: #333; padding: 10px;">wss://io.dexscreener.com/dex/screener/v4/pairs/h24/1?rankBy[key]=trendingScoreH6&rankBy[order]=desc</pre>
                </li>
                <li>You need to ping Dex for the desired time. Use a cron job. ⏰</li>
               <li><span style="font-weight: bold; color: red;">NOTE:</span> This code is finetuned for Solana Tokens</li>
            </ol>
        </body>
    """

@app.route('/dex', methods=['GET'])
def dex():
    try:
        new = DexBot(Api, ID, chain=False)
        mes = new.format_token_data()  # This will connect and send to Telegram immediately

        mes_json = json.dumps(mes)
        
        return f'''
            <body style="background-color:black; font-family: Arial, sans-serif; color:white">
                <div style="text-align: center;">
                    <h1 style="color:lightblue">Dex screener trending data 📋</h1>
                </div>
                <div style="padding: 20px; text-align: center;">
                    <pre style="
                        background-color: #333;
                        padding: 10px;
                        margin: 0 auto;
                        display: inline-block;
                        text-align: left;
                        color: white;
                        border-radius: 5px;
                        width: 70%;
                        word-wrap: break-word;
                        white-space: pre-wrap;
                        overflow-y: scroll;
                        "> 
                        {mes}
                    </pre>
                </div>

            <script> console.log({mes_json})</script>
            </body>
        '''
            
    except Exception as e:
        print(e)
        return f'''
            <body style="background-color:black; color:red; font-family: Arial, sans-serif; text-align: center; padding: 20px;">
                <h2>Error occurred</h2>
                <p>{str(e)}</p>
                <p>Unable to send message.</p>
            </body>
            '''

@app.route('/ui', methods=['GET'])
def ui():
    try:
        # Fetch the token data
        new = DexBot(Api, ID, chain=False)
        mes = new.format_token_data()  # This will connect and fetch the token data
        tokens = json.loads(mes)  # Parse JSON data into a Python object
        tokens = tokens.get("data")
        
        token_cards = ""
        for token in tokens:
            # Safely extract data with default values
            base_token = token.get("baseToken", {})
            volume = token.get("volume", {})
            price_change = token.get("priceChange", {})
            liquidity = token.get("liquidity", {})
            txns = token.get("txns", {}).get("h24", {})
            info = token.get("info", {})
            boosts = token.get("boosts", {})

            token_cards += f'''
            <div class="max-w-4xl mx-auto p-6 bg-gray-900 rounded-xl shadow-2xl mb-6">
                <div class="bg-gray-800 rounded-xl p-6">
                    <!-- Header -->
                    <div class="flex items-start gap-6 mb-6">
                        <img src="{info.get('imageUrl', 'https://via.placeholder.com/50')}" 
                             alt="{base_token.get('symbol', 'TOKEN')}" 
                             class="w-16 h-16 rounded-full">
                        <div class="flex-grow">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h2 class="text-2xl font-bold text-white">
                                        {base_token.get('name', 'Unknown Token')} ({base_token.get('symbol', 'TOKEN')})
                                    </h2>
                                    <div class="flex items-center gap-2 text-gray-400">
                                        <span class="capitalize">{token.get('chainId', 'unknown')}</span>
                                        <span>•</span>
                                        <span class="capitalize">{token.get('dexId', 'unknown')}</span>
                                        <div class="flex items-center gap-1 bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded">
                                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
                                            </svg>
                                            {boosts.get('active', 0)}
                                        </div>
                                    </div>
                                </div>
                                <a href="{token.get('url', '#')}" 
                                   target="_blank"
                                   class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors">
                                    View on Dex
                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/>
                                    </svg>
                                </a>
                            </div>
                        </div>
                    </div>

                    <!-- Main Stats Grid -->
                    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
                        <div class="bg-gray-800 rounded-lg p-3">
                            <div class="flex items-center gap-2 text-gray-400 text-sm mb-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                </svg>
                                Price USD
                            </div>
                            <div class="text-lg font-bold {float(price_change.get('h24', 0))} > 0 ? 'text-green-400' : 'text-red-400'">
                                {float(token.get('priceUsd', 0)):.5f}
                            </div>
                            <div class="text-sm text-gray-400">
                                24h: {float(price_change.get('h24', 0)):.2f}%
                            </div>
                        </div>

                        <div class="bg-gray-800 rounded-lg p-3">
                            <div class="flex items-center gap-2 text-gray-400 text-sm mb-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                                </svg>
                                24h Volume
                            </div>
                            <div class="text-lg font-bold">
                                {float(volume.get('h24', 0)):,.2f}
                            </div>
                        </div>

                        <div class="bg-gray-800 rounded-lg p-3">
                            <div class="flex items-center gap-2 text-gray-400 text-sm mb-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
                                </svg>
                                Liquidity
                            </div>
                            <div class="text-lg font-bold">
                                {float(liquidity.get('usd', 0)):,.2f}
                            </div>
                        </div>

                        <div class="bg-gray-800 rounded-lg p-3">
                            <div class="flex items-center gap-2 text-gray-400 text-sm mb-1">
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"/>
                                </svg>
                                Market Cap
                            </div>
                            <div class="text-lg font-bold">
                                {float(token.get('marketCap', 0)):,.2f}
                            </div>
                        </div>
                    </div>

                    <!-- Trading Activity -->
                    <div class="bg-gray-900 rounded-lg p-4 mb-6">
                        <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
                            </svg>
                            24h Trading Activity
                        </h3>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="flex items-center gap-3">
                                <svg class="w-5 h-5 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                                </svg>
                                <div>
                                    <div class="text-sm text-gray-400">Buys</div>
                                    <div class="font-bold">{txns.get('buys', 0):,}</div>
                                </div>
                            </div>
                            <div class="flex items-center gap-3">
                                <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 17l-5-5m0 0l5-5m-5 5h12"/>
                                </svg>
                                <div>
                                    <div class="text-sm text-gray-400">Sells</div>
                                    <div class="font-bold">{txns.get('sells', 0):,}</div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Social Links -->
                    <div class="flex gap-3">
                        {' '.join([
                            f"""<a href="{social.get('url', '#')}" target="_blank" class="bg-gray-700 hover:bg-gray-600 p-2 rounded-lg transition-colors">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                        d="{'M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z' 
                                        if social.get('type') == 'twitter' 
                                        else 'M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z'}"/>
                                </svg>
                            </a>
                            """ for social in info.get('socials', [])
                        ])}
                    </div>

                </div>
            </div>
            '''

        return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <script src="https://cdn.tailwindcss.com"></script>
                <title>Token Dashboard</title>
            </head>
            <body class="bg-gray-900 text-white min-h-screen p-6">
                <div class="container mx-auto">
                    {token_cards}
                </div>
            </body>
            </html>
        '''
    except Exception as e:
        return f'''
            <body style="background-color:black; color:red; font-family: Arial, sans-serif; text-align: center; padding: 20px;">
                <h2>Error occurred</h2>
                <p>{str(e)}</p>
                <p>Unable to process token data.</p>
            </body>
        '''
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
