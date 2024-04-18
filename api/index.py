from http.server import BaseHTTPRequestHandler
import telebot

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        bot = telebot.TeleBot("6227128550:AAGTVw8ERRRAdZK0kSaRqXLkEXeloIXGg_0")
        bot.send_message(chat_id="-1001802310005", text="Hi there bitch it worked")
        self.wfile.write('Hello, world!'.encode('utf-8'))
        return
