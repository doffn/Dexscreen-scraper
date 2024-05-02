from flask import Flask, request
from api.main_code import *  # Assuming main_code defines reviewer()
from api.dex import *
import threading

app = Flask(__name__)


addr = os.environ['ADDRESS']
Api = os.environ["API"]
ID = "-1001873201570"


@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'
 

@app.route('/service', methods=['GET', 'POST'])
def service():
    main_function()
    if request.method == 'POST':
        try:
            # Submit the review task asynchronously
            # For now, return a success message without time estimate
            return '<body style="background-color:black; color:white;">Review submitted. Please wait for results.</body>'

        except Exception as e:
            print(f"Error in service endpoint: {e}")
            return '<body style="background-color:black; color:white;">An error occurred.</body>'
    else:
        return '<body style="background-color:black; color:white;">Service endpoint accessed</body>'

@app.route('/dex', methods=['GET', 'POST'])
def dex():
    try:
        new = DexBot(Api, ID)
        mes = new.token_getter()
        new.tg_send(str(mes))
    except Exception as e:
        print(e)

    if request.method == 'POST':
        try:
            # Submit the review task asynchronously
            # For now, return a success message without time estimate
            return '<body style="background-color:black; color:white;">dex screen</body>'

        except Exception as e:
            print(f"Error in service endpoint: {e}")
            return '<body style="background-color:black; color:white;">An error occurred.</body>'
    else:
        return '<body style="background-color:black; color:white;">Service endpoint accessed</body>'


if __name__ == '__main__':
    app.run()
