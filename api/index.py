from flask import Flask, request
from api.main_code import *
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("YOUR_TOKEN")

@app.route('/', methods=['GET'])
def root():
    return '\x1b[42m\x1b[34mHello, world! This is the root endpoint.\x1b[0m'

@app.route('/service', methods=['GET', 'POST'])
def service():
    main_function()
    if request.method == 'POST':
        try:
            # Code for the '/service' POST endpoint
            # Perform any necessary actions or computations
            
            return '\x1b[42m\x1b[34mService endpoint accessed\x1b[0m'
        except Exception as e:
            print(e)
            return '\x1b[42m\x1b[34mAn error occurred\x1b[0m'
    else:
        return '\x1b[42m\x1b[34mService endpoint accessed\x1b[0m'

if __name__ == '__main__':
    app.run()
