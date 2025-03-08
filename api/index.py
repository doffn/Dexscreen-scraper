from flask import Flask, request, render_template
import json
from api.dex import DexBot  # Ensure DexBot is correctly imported

app = Flask(__name__, template_folder='../templates')

# Define Api and ID as needed for your DexBot initialization
Api = "YOUR_API"  # Replace with your actual API or configuration
ID = "YOUR_ID"    # Replace with your actual ID or token

@app.route('/', methods=['GET'])
def root():
    return render_template("index.html")

@app.route('/dex', methods=['GET'])
def dex():
    try:
        # Retrieve the filter string from the query parameter
        generated_text = request.args.get('generated_text', '')
        if not generated_text:
            return "<h2>No generated text provided.</h2>", 400

        # Initialize DexBot with the generated filter string
        new_bot = DexBot(Api, ID, generated_text)
        mes = new_bot.format_token_data()

        # Format the response JSON nicely for display
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
