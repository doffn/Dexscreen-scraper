from flask import Flask, request
from flask_misaka import markdown
from api.dex import *
import threading
import asyncio

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
        # Fetch and format the Dex screener data
        new = DexBot(Api, ID, chain=False)
        token_data = new.format_token_data()  # Assuming it returns a list of tokens
        token_data_json = json.dumps(token_data)  # Convert to JSON for JS

        # Generate the HTML response
        return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Dex Screener Tokens</title>
                <style>
                    body {{
                        background-color: #1e1e1e;
                        color: #f0f0f0;
                        font-family: 'Arial', sans-serif;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 900px;
                        margin: 50px auto;
                        padding: 20px;
                        background-color: #282c34;
                        border-radius: 8px;
                        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
                    }}
                    h1 {{
                        color: #61dafb;
                        text-align: center;
                        margin-bottom: 20px;
                    }}
                    .token-list {{
                        list-style: none;
                        padding: 0;
                        margin: 0;
                    }}
                    .token-item {{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 10px;
                        margin-bottom: 10px;
                        background-color: #333;
                        border-radius: 5px;
                    }}
                    .token-item img {{
                        width: 40px;
                        height: 40px;
                        border-radius: 50%;
                        margin-right: 10px;
                    }}
                    .token-info {{
                        display: flex;
                        align-items: center;
                    }}
                    .token-metrics {{
                        text-align: right;
                    }}
                    .token-metrics span {{
                        display: block;
                    }}
                    .error {{
                        color: #e74c3c;
                        text-align: center;
                        font-weight: bold;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Dex Screener Tokens 📊</h1>
                    <ul class="token-list" id="tokenList"></ul>
                </div>

                <script>
                    const tokenData = {token_data_json}; // Injecting token data from Python

                    const tokenList = document.getElementById('tokenList');

                    tokenData.forEach(token => {{
                        const tokenItem = document.createElement('li');
                        tokenItem.className = 'token-item';

                        tokenItem.innerHTML = `
                            <div class="token-info">
                                <img src="{token.get('image_url', '')}" alt="{token.get('name', 'Token')}">
                                <div>
                                    <strong>${{token.name}} (${token.symbol})</strong><br>
                                    <a href="${{token.dex_url}}" target="_blank" style="color: #61dafb;">View on Dex</a>
                                </div>
                            </div>
                            <div class="token-metrics">
                                <span>Total Profit: $${{parseFloat(token.total_profit).toFixed(2)}}</span>
                                <span>Bought Transactions: ${{token.metrics.boughtTxn}}</span>
                            </div>
                        `;

                        tokenList.appendChild(tokenItem);
                    }});
                </script>
            </body>
            </html>
        '''
    except Exception as e:
        return f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Error</title>
                <style>
                    body {{
                        background-color: #1e1e1e;
                        color: #f0f0f0;
                        font-family: 'Arial', sans-serif;
                        text-align: center;
                        padding: 50px;
                    }}
                    .error {{
                        color: #e74c3c;
                        font-weight: bold;
                        font-size: 1.2rem;
                    }}
                </style>
            </head>
            <body>
                <h1 class="error">Error Occurred 🚨</h1>
                <p>{str(e)}</p>
                <p>Unable to process the request at this time.</p>
            </body>
            </html>
        '''


if __name__ == '__main__':
    app.run(debug=True)
