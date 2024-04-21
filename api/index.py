from flask import Flask, request
from api.main_code import *
import threading
import telebot

app = Flask(__name__)
bot = telebot.TeleBot("YOUR_TOKEN")

def run_main_function():
    main_function()
    
@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'

@app.route('/service', methods=['GET', 'POST'])
def service():
    #thread1 = threading.Thread(target=main_function)
    # Set the thread as a daemon
    # Create a thread targeting the run_main_function
    thread1 = threading.Thread(target=run_main_function)
    thread1.start()
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
