from http.server import BaseHTTPRequestHandler
import telebot

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        bot = telebot.TeleBot("5628135628:AAH_41TGhCSaK6lq5UFK7fjlaq4Jq8dYRBA")
        bot.send_message(chat_id="5628135628", text="Hi there bitch it worked")
        self.wfile.write('Hello, world!'.encode('utf-8'))
        print("well done")
        return
