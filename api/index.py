from flask import Flask, request
from api.main_code import *
import telebot

from sanic import Sanic
from sanic.response import json
app = Sanic()
 
 
@app.route('/')
@app.route('/<path:path>')
async def index(request, path=""):
    return json({'hello': path})
