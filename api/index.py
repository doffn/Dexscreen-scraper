from flask import Flask, request
from api.main_code import *
import threading
import telebot
app = Flask(__name__)
bot = telebot.TeleBot("YOUR_TOKEN")


    
@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'

@app.route('/service', methods=['GET', 'POST'])
def service():
    @app.after_response
    def add_close_action(response):
        @response.call_on_close
        def process_after_request():
            main_function()
    
    if request.method == 'POST':
        try:
            # Code for the '/service' POST endpoint
            # Perform any necessary actions or computations
            
            return '<body style="background-color:black; color:white;">Service endpoint accessed</body>'
        except Exception as e:
            print(e)
            return '<body style="background-color:black; color:white;">An error occurred</body>'
    else:
        return '<body style="background-color:black; color:white;">Service endpoint accessed</body>'

if __name__ == '__main__':
    app.run()
