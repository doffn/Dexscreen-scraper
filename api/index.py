from http.server import BaseHTTPRequestHandler
import telebot

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        try:
            bot = telebot.TeleBot("6098595418:AAFpqdwwoMXPPv8VxroKZIejJ5LYky8rtGY")
            bot.send_message(chat_id="-1001873201570", text="Hi there bitch it worked")
        except Exception as e:
            print(e)
        self.wfile.write('Hello, world!'.encode('utf-8'))
        print("well done")
        return
