from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Home route that renders the HTML form
@app.route('/', methods=['GET', 'POST'])
def home():
    converted_value = None
    if request.method == 'POST':
        try:
            huf_amount = float(request.form['huf_amount'])
            converted_value = convert_currency(huf_amount)
        except ValueError:
            converted_value = "Invalid input"
    return render_template('index.html', converted_value=converted_value)

# Function to connect to the API and convert HUF to EUR
def convert_currency(amount_huf):
    try:
        # Make a request to the exchange rate API (replace with a valid API key)
        api_key = 'feec8b7611be09b0cad59a2b'
        url = f'https://api.apilayer.com/exchangerates_data/convert?from=HUF&to=EUR&amount={amount_huf}&apikey={api_key}'
        response = requests.get(url)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('result', "Conversion error")
        else:
            return "API Error"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
