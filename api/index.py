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
        mes = new.token_getter()
        
        # Send to Telegram in a separate thread
        def send_to_telegram():
            new.tg_send(mes)
        
        threading.Thread(target=send_to_telegram).start()
        
        return f'''
            <body style="background-color:black; font-family: Arial, sans-serif; color:white">
                <div style="text-align: center;">
                    <h1 style="color:lightblue">Dex screener trending data 📋</h1>
                </div>
                <div style="padding: 20px; text-align: center;">
                    <pre style="background-color: #333; padding: 10px; margin: 0 auto; display: inline-block; text-align: left; color: white; border-radius: 5px;">{mes}</pre>
                </div>
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

if __name__ == '__main__':
    app.run(debug=True)