"""from flask import Flask, request
from api.main_code import *  # Assuming main_code defines reviewer()
import threading
import asyncio


app = Flask(__name__)


thread1 = threading.Thread(target=main_function)
    


@app.route('/', methods=['GET'])
def root():
    return '<body style="background-color:black; color:white; font-family: Arial, sans-serif;">Hello User, This is my API</body>'
 


@app.route('/service', methods=['GET', 'POST'])
def service():
    #asyncio.create_task(main_function())
    thread1.start()
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


if __name__ == '__main__':
    app.run()
"""

import http.server
import socketserver
import threading
import random

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello. I am alive!')

def run():
    port = random.randint(8000, 9000)  # Generate a random port number between 8000 and 9000
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print(f'Server started on port {port}')
        httpd.serve_forever()

def keep_alive():
    t = threading.Thread(target=run)
    t.start()