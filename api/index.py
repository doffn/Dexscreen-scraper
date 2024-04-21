from flask import Flask, request
from api.main_code import *
import telebot


from flask import Flask, request
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("YOUR_TOKEN")

@app.route('/', methods=['GET'])
def root():
    reviewer()
    return 'Hello, world! This is the root endpoint.'

@app.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        try:
            # Code for the '/service' POST endpoint
            # Perform any necessary actions or computations
            main_function()
            return 'Service endpoint accessed'
        except Exception as e:
            print(e)
            return 'An error occurred'
    else:
        return 'Service endpoint accessed'



if __name__ == '__main__':
    app.run()
