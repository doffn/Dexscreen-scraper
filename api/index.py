from flask import Flask, request
from api.main_code import *  # Assuming main_code defines reviewer()
import threading
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

executor = ThreadPoolExecutor()


def run_main_function():
    try:
        # Perform the review
        result = reviewer()
        # Handle the review result here (e.g., logging, storing)
        return result
    except Exception as e:
        print(f"Error during review: {e}")
        return "Review failed"


@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'


@app.route('/service', methods=['GET', 'POST'])
def service():
    if request.method == 'POST':
        try:
            # Submit the review task asynchronously
            future = executor.submit(run_main_function)

            # Consider using Flask-RESTful for better asynchronous responses,
            # or implement your own mechanism to wait for the review result.

            # For now, return a success message without time estimate
            return '<body style="background-color:black; color:white;">Review submitted. Please wait for results.</body>'
        except Exception as e:
            print(f"Error in service endpoint: {e}")
            return '<body style="background-color:black; color:white;">An error occurred.</body>'
    else:
        return '<body style="background-color:black; color:white;">Service endpoint accessed</body>'


if __name__ == '__main__':
    app.run()
