from flask import Flask, request
from flask_misaka import markdown
from api.dex import *
import threading

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
        new = DexBot(Api, ID, chain=False) # define the chain if you desire a specific chain eg. ETH, SOL, BASE
        mes = new.token_getter()
        new.tg_send(str(mes))  
    except Exception as e:
        print(e)
        return f'<body style="background-color:black; color:red;">Error occurred: {str(e)}. Unable to send message.</body>'

    return f'''
        <body style="background-color:black; font-family: Arial, sans-serif; color:white">
            <div padding: 20px;">
                <pre style="background-color: #333; padding: 10px;">{markdown(mes)}</pre>
            </div>

        </body>
        '''

if __name__ == '__main__':
    app.run()