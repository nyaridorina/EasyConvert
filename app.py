import os
from flask import Flask, request, render_template
import requests
import logging

app = Flask(__name__)

# Set up logging for errors
logging.basicConfig(level=logging.ERROR)

# Home route that renders the HTML form
@app.route('/', methods=['GET', 'POST'])
def home():
    converted_value = None
    api_error = None
    if request.method == 'POST':
        try:
            huf_amount = float(request.form['huf_amount'])
            if huf_amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            converted_value = convert_currency(huf_amount)
            if "API Error" in converted_value or "Error:" in converted_value:
                api_error = converted_value
                converted_value = None
        except ValueError:
            api_error = "Invalid input. Please enter a valid number greater than zero."
    return render_template('index.html', converted_value=converted_value, api_error=api_error)

# Function to connect to the API and convert HUF to EUR
def convert_currency(amount_huf):
    try:
        # Make a request to the exchange rate API (replace with a valid API key)
        api_key = os.getenv('EXCHANGE_API_KEY')
        if not api_key:
            raise ValueError("API key is missing. Please set the EXCHANGE_API_KEY environment variable.")
        
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/HUF/EUR/{amount_huf}'
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('conversion_result', "Conversion error")
        else:
            return f"API Error: {response.status_code} - {response.reason}"
    except Exception as e:
        logging.error(f"Error occurred during currency conversion: {e}")
        return "An error occurred. Please try again later."

if __name__ == '__main__':
    app.run(debug=True)
