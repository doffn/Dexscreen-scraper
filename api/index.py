from flask import Flask, request, render_template
from api.dex import *
import json

app = Flask(__name__, template_folder='../templates')

@app.route('/', methods=['GET'])
def root():
    return render_template("index.html")

@app.route('/dex', methods=['GET'])
def dex():
    try:
        new = DexBot(Api, ID, chain=False)
        mes = new.format_token_data()  # This will connect and send to Telegram immediately

        mes_json = json.dumps(json.loads(mes), indent=4)
        
        return render_template("dex.html", mes=mes_json)
            
    except Exception as e:
        print(e)
        return f'''
            <body style="background-color:black; color:red; font-family: Arial, sans-serif; text-align: center; padding: 20px;">
                <h2>Error occurred</h2>
                <p>{str(e)}</p>
                <p>Unable to send message.</p>
            </body>
        '''



if __name__ == '__main__':
    app.run(debug=True)
