from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Home route that renders the HTML form
@app.route('/', methods=['GET', 'POST'])
def home():
    converted_value = None
    api_error = None
    if request.method == 'POST':
        try:
            huf_amount = float(request.form['huf_amount'])
            converted_value = convert_currency(huf_amount)
            if "API Error" in converted_value or "Error:" in converted_value:
                api_error = converted_value
                converted_value = None
        except ValueError:
            api_error = "Invalid input. Please enter a valid number."
    return render_template('index.html', converted_value=converted_value, api_error=api_error)

# Function to connect to the API and convert HUF to EUR
def convert_currency(amount_huf):
    try:
        # Make a request to the exchange rate API (replace with a valid API key)
        api_key = 'feec8b7611be09b0cad59a2b'
        url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/HUF/EUR/{amount_huf}'
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('conversion_result', "Conversion error")
        else:
            return f"API Error: {response.status_code} - {response.reason}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
