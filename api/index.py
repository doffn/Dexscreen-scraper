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
        tokens = json.loads(json.dumps(mes)).get("data")  # Parse JSON data into a Python object

        print(len(tokens))

        token_rows = ""
        for token in tokens:
            # Extract data safely and handle missing values
            if isinstance(token, dict):
                chain_id = token.get("chainId", "Unknown Chain")
                dex_id = token.get("dexId", "Unknown Dex")
                url = token.get("url", "#")
                base_token = token.get("baseToken", {})
                price_usd = token.get("priceUsd", "N/A")
                volume = token.get("volume", {}).get("h24", 0)
                image_url = token.get("info", {}).get("imageUrl", "https://via.placeholder.com/50")
                socials = token.get("info", {}).get("socials", [])
                token_name = base_token.get("name", "Unknown Token")
                token_symbol = base_token.get("symbol", "N/A")

                # Create HTML rows for each token
                token_rows += f'''
                    <div class="token-row">
                        <div class="token-image">
                            <img src="{image_url}" alt="{token_symbol}">
                        </div>
                        <div class="token-info">
                            <h3>{token_name} ({token_symbol})</h3>
                            <p>Price: $ {float(price_usd):.2f}</p>
                            <p>Volume (24h): $ {int(volume):,}</p>
                            <p>Chain: {chain_id}, Dex: {dex_id}</p>
                        </div>
                        <div class="token-links">
                            <a href="{url}" target="_blank" class="btn">View on Dex</a>
                            {''.join([f'<a href="{social.get("url", "#")}" target="_blank" class="icon-{social.get("type", "link")}"><i class="bx bxl-{social.get("type", "link")}"></i></a>' for social in socials])}
                        </div>
                    </div>
                '''
            else:
                # Handle cases where token is not a dictionary (optional)
                token_rows += f'<div class="token-row">Error processing token data</div>'

        return f'''
            <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: black;
                        color: white;
                        margin: 0;
                        padding: 0;
                    }}
                    .token-container {{
                        display: flex;
                        flex-direction: column;
                        gap: 1rem;
                        padding: 1rem;
                    }}
                    .token-row {{
                        display: flex;
                        gap: 1rem;
                        border: 1px solid white;
                        padding: 1rem;
                        border-radius: 8px;
                        background: #333;
                    }}
                    .token-image img {{
                        width: 50px;
                        height: 50px;
                        border-radius: 50%;
                    }}
                    .token-info {{
                        flex-grow: 1;
                    }}
                    .token-links a {{
                        margin-right: 0.5rem;
                        text-decoration: none;
                        color: #fff;
                        background: #007bff;
                        padding: 0.5rem 1rem;
                        border-radius: 5px;
                    }}
                </style>
            </head>
            <body>
                <div class="token-container">
                    {token_rows}
                </div>
            </body>
            </html>
        '''
    except Exception as e:
        return f"<h1>Error: {str(e)}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
