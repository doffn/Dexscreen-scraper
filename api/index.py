from flask import Flask, request
from api.main_code import *
import threading
from concurrent.futures import ThreadPoolExecutor
import telebot
app = Flask(__name__)
bot = telebot.TeleBot("YOUR_TOKEN")


executor = ThreadPoolExecutor()

@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'

@app.route('/service', methods=['GET', 'POST'])
def service():
    """
    thread1 = threading.Thread(target=main_function)
    thread1.setDaemon(True)
    thread1.join()
    thread1.start()"""
    # Submit the task to the thread pool for asynchronous execution
    executor.submit(run_main_function)

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

def run_main_function():
    # Simulate a time-consuming task
    main_function()


if __name__ == '__main__':
    app.run()
