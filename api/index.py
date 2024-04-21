from flask import Flask, request
from api.main_code import *
import threading
import telebot
import asyncio

app = Flask(__name__)
bot = telebot.TeleBot("YOUR_TOKEN")

async def main_task():
    main_function()
    await asyncio.sleep(10)  # Example: Sleep for 10 seconds
    
@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'

@app.route('/service', methods=['GET', 'POST'])
def service():
    #thread1 = threading.Thread(target=main_function)
    # Set the thread as a daemon
    # Create an event loop and run the main_task asynchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main_task())
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
