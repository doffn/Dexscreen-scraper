from flask import Flask, request
from api.dex import *
import threading

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This will scrape from Dexscreener trending tokens by running the /dex path</body>'

@app.route('/dex', methods=['GET'])
def dex():
    try:
        new = DexBot(Api, ID)
        mes = new.token_getter()
        new.tg_send(str(mes))
    except Exception as e:
        print(e)

    return '<body style="background-color:black; color:white;">dex endpoint</body>'


if __name__ == '__main__':
    app.run()
