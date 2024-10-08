from flask import Flask, request, render_template
from DividendCalculator import data, Prediction  # Assuming your refactored classes are in this module
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-etf-data', methods=['POST'])
def get_etf_data():
    ticker = request.form['ticker']
    years = int(request.form['years'])
    
    # Instantiate the Data class
    data_instance = data()    
    # Create a dictionary to hold the ETF data
    etf_data = {}
    etf_data['price'] = data_instance.get_etf_price(ticker)
    etf_data['dividend_yield'] = data_instance.get_dividend_yield(ticker)
    etf_data['dividend_rate'] = data_instance.get_dividend_rate(ticker)
    etf_data['growth'] = data_instance.get_etf_growth(ticker)
    etf_data['dividend_payouts'] = data_instance.get_dividend_payouts(ticker)

    # Instantiate Prediction class with the data instance
    prediction_instance = Prediction(data_instance)  # Passing the data instance to Prediction
    etf_data['future_price'] = prediction_instance.get_future_ETF_price(ticker, years)  # Using the instance
    etf_data['future_dividend_yield'] = prediction_instance.get_future_dividend_yield(ticker, years)  # Using the instance

    # Close the WebDriver after scraping

    return render_template('result.html', etf_data=etf_data, years=years, ticker=ticker)

if __name__ == '__main__':
    app.run(debug=True)
