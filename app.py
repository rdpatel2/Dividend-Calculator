from flask import Flask, request, render_template
from DividendCalculator import data, Prediction  # Replace 'your_module' with the actual name of your module

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-etf-data', methods=['POST'])
def get_etf_data():
    ticker = request.form['ticker']
    years = int(request.form['years'])
    etf_data = {}
    
    etf_data['price'] = data.get_etf_price(ticker)
    etf_data['dividend_yield'] = data.get_dividend_yield(ticker)
    etf_data['dividend_rate'] = data.get_dividend_rate(ticker)
    etf_data['growth'] = data.get_etf_growth(ticker)
    etf_data['dividend_payouts'] = data.get_dividend_payouts(ticker)

    etf_data['future_price'] = Prediction.get_future_ETF_price(ticker, years)  # Example: 5 years into the future
    etf_data['future_dividend_yield'] = Prediction.get_future_dividend_yield(ticker, years)  # Example: 5 years into the future

    return render_template('result.html', etf_data=etf_data, years=years, ticker=ticker)

if __name__ == '__main__':
    app.run(debug=True)
