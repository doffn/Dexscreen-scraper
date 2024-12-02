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
                    <pre style="background-color: #333; padding: 10px;">wss://io.dexscreener.com/dex/screener/pairs/h24/1?rankBy[key]=trendingScoreH1&rankBy[order]=desc&filters[liquidity][min]=1000&filters[pairAge][max]=24</pre>
                </li>
                <li>You need to ping Dex for the desired time. Use a cron job. ⏰</li>
            </ol>
        </body>
    """

@app.route('/dex', methods=['GET'])
def dex():
    try:
        new = DexBot(Api, ID, chain=False)
        mes = new.format_token_data()  # This will connect and send to Telegram immediately
        
        # Format the mes string as JSON
        formatted_json = json.dumps(json.loads(mes), indent=2)

        return f'''
            <html>
            <head>
                <style>
                    body {{
                        background-color: black;
                        font-family: Arial, sans-serif;
                        color: white;
                        text-align: center;
                    }}
                    h1 {{
                        color: lightblue;
                    }}
                    .json-container {{
                        background-color: #333;
                        padding: 20px;
                        margin: 20px auto;
                        display: inline-block;
                        text-align: left;
                        color: white;
                        border-radius: 5px;
                        width: 80%;
                        max-height: 500px;
                        overflow-y: scroll;
                        word-wrap: break-word;
                        white-space: pre-wrap;
                    }}
                    .copy-btn {{
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        font-size: 16px;
                        border-radius: 5px;
                        cursor: pointer;
                        margin-top: 10px;
                    }}
                    .copy-btn:hover {{
                        background-color: #45a049;
                    }}
                </style>
            </head>
            <body>
                <div>
                    <h1>Dex screener trending data 📋</h1>
                </div>
                <div class="json-container" id="jsonContainer">
                    {formatted_json}
                </div>
                <button class="copy-btn" id="copyBtn">Copy JSON</button>
                
                <script>
                    // Copy JSON to clipboard functionality
                    document.getElementById('copyBtn').addEventListener('click', function() {{
                        var jsonContainer = document.getElementById('jsonContainer');
                        var range = document.createRange();
                        range.selectNode(jsonContainer);
                        window.getSelection().removeAllRanges();
                        window.getSelection().addRange(range);
                        document.execCommand('copy');
                        window.getSelection().removeAllRanges();
                    }});
                </script>
            </body>
            </html>
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

if __name__ == '__main__':
    app.run(debug=True)