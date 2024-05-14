## API Documentation 

This serves as a guide for the provided Flask API .

# **Introduction**

This API offers functionalities related to reviews and token information retrieval . The code uses Flask for the web framework and interacts with an external service (DexScreener) through websockets for retrieving token data .

# **API Endpoints**

* **Root (`/`)** (GET):
    * Returns a basic message acknowledging a user's access to the API.    *Cool!* 

* **Service (`/service`)** (GET, POST):
    * Triggers the `main_function` responsible for review processing (assumed functionality based on import). 
    * Handles GET and POST requests:
        * **GET:** Returns a message indicating the service endpoint has been accessed.  *Service endpoint accessed! ✅*
        * **POST:** Submits a review task asynchronously and returns a success message without a time estimate. In case of errors, an error message is returned.  *Review submitted. Please wait for results. ⏱️*  *An error occurred. ⚠️*

* **Dex (`/dex`)** (GET):
    * Retrieves token information from DexScreener. 
    * If successful, returns a message indicating the dex endpoint has been accessed. In case of errors, an error message is printed.  *Dex endpoint accessed! ✅*  *Error! ⚠️*

# **Code Structure**

* **Flask App Setup**
    * Initializes the Flask application and defines routes for the API endpoints. 

* **Routes**
    * Each endpoint definition includes a docstring explaining its functionality and behavior for different HTTP methods (GET, POST). 
    * Error handling is implemented to capture exceptions and return appropriate error messages.   

# **External Libraries**

* Flask: Web framework for building web applications ([https://flask.palletsprojects.com/en/2.3.x/](https://flask.palletsprojects.com/en/2.3.x/)) 
* `api.main_code`: Assumed to contain the `reviewer` function for review processing.  ️‍♀️ 
* `api.dex`: Assumed to contain functionalities related to DexBot class and token retrieval.   
* threading: Enables running asynchronous tasks.  
* websockets: Library for establishing websocket connections ([https://readthedocs.org/projects/websockets/](https://readthedocs.org/projects/websockets/)) ️
* telebot: Library for interacting with the Telegram bot API ([https://pypi.org/project/pyTelegramBotAPI/](https://pypi.org/project/pyTelegramBotAPI/))  
* datetime: Library for working with date and time objects (built-in Python module).  ️
* os: Library for interacting with the operating system (built-in Python module).  ️

# **Environment Variables**

* **API:** Stores the Telegram bot API key.  
* **ID:** Stores the Telegram channel ID for sending messages.  

# **DexBot Class**

This class facilitates communication with DexScreener for retrieving token information. 

* **__init__(self, api_key, channel_id, chain=False, max_token=10):**
    * Initializes the class with the provided API key, channel ID, optional chain parameter (for filtering tokens by chain), and the maximum number of tokens to retrieve.   ℹ️

* **connect(self):** (Asynchronous function)
    * Establishes a websocket connection with DexScreener and returns the initial response data.  ️ ✨

* **tg_send(self, message):**
    * Sends a message to the specified Telegram channel using the Telegram bot API.   

* **token_getter(self):**
    * Retrieves token information from DexScreener using a websocket connection.
    * Parses the response data and formats it into a markdown string containing details like token name, price, market cap, etc.  🪄 ✨
    * Returns the formatted markdown string containing token information.  


## Credits 🙌

This project was created by **Dawit Neri**

## Support 💬

If you encounter any issues or have any questions, feel free to reach out to dawitneri888@gmail.com or open an issue in the GitHub repository.  

  
