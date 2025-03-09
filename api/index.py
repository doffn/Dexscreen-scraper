from flask import Flask, request, render_template
import json
from api.dex import *  # Ensure DexBot is correctly imported

app = Flask(__name__, template_folder='../templates')


@app.route('/', methods=['GET'])
def root():
    return render_template("index.html")


@app.route('/dex', methods=['GET'])
def dex():
    try:
        # Default URL for Dex
        text = "wss://io.dexscreener.com/dex/screener/v4/pairs/h24/1?rankBy[key]=trendingScoreH6&amp;rankBy[order]=desc"
        
        # Retrieve the filter string from the query parameter
        generated_text = request.args.get('generated_text', '')
        
        # If there's a generated_text, append it to the URL, but only if it's not empty
        if generated_text:
            text += generated_text
        
        # Print the generated_text for debugging
        print(generated_text)

        # Initialize DexBot with the generated filter string (or default if none)
        new_bot = DexBot(Api, text)  # Ensure this matches your DexBot constructor
        mes = new_bot.format_token_data()

        # If mes is already a JSON string, no need for json.loads
        if isinstance(mes, str):
            try:
                mes_json = json.dumps(json.loads(mes), indent=4)
            except json.JSONDecodeError:
                mes_json = f"Error decoding JSON: {mes}"
        else:
            mes_json = json.dumps(mes, indent=4)  # Assuming mes is already a dictionary or similar

        # Render the page with the formatted data
        return render_template("dex.html", mes=mes_json)

    except Exception as e:
        # In case of error, display the error message
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
