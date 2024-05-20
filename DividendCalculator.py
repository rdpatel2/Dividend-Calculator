import requests
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask

class data:

  def get_etf_price(ticker): # Gets the current price of the ETF
    url = f"https://etfdb.com/etf/{ticker}/#etf-ticker-profile"
    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Not a Divdend Paying ETF")
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find("span", class_="stock-quote-data").text
    price = price.replace("\n", "")
    price = price.replace("$", "")
    return float(price)

  def get_dividend_yield(ticker): # Gets the annual dividend yield of the ETF
    dividendURL = f"https://etfdb.com/etf/{ticker}/#etf-ticker-valuation-dividend"
    response = requests.get(dividendURL)
    if response.status_code != 200:
      raise Exception("Not a Divdend Paying ETF")
    soup = BeautifulSoup(response.text, "html.parser")
    dividendYields = soup.find_all("td", class_="center")
    dividendYield = dividendYields[70].text
    dividendYield = dividendYield.replace("\n", "")
    dividendYield = dividendYield.replace("$", "")

    return float(dividendYield)

  def get_dividend_rate(ticker): # Gets the dividend percentage of the ETF
    price = data.get_etf_price(ticker)
    dividendYield = data.get_dividend_yield(ticker)
    dividendRate = dividendYield / price
    return round(dividendRate, 4)
  
  def get_etf_growth(ticker): # Gets the YTD growth of the ETF
    url = f"https://etfdb.com/etf/{ticker}/#performance"
    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Not a Divdend Paying ETF")
    soup = BeautifulSoup(response.text, "html.parser")
    growthPercent = soup.find_all("td", class_="col-lg-4 col-xs-4")
    growth = growthPercent[6].text
    growth = growth.replace("\n", "")
    growth = growth.replace("%", "")
    return float(growth) / 100

  def get_dividend_payouts(ticker): # Gets the price per dividend paid
    url = f"https://etfdb.com/etf/{ticker}/#etf-ticker-valuation-dividend"
    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Not a Divdend Paying ETF")
    soup = BeautifulSoup(response.text, "html.parser")
    payouts = soup.find_all("td", class_="center")
    payout = payouts[64].text
    payout = payout.replace("\n", "")
    payout = payout.replace("$", "")
    return float(payout)

  def get_num_payouts(ticker):
    return (data.get_dividend_yield(ticker) / data.get_dividend_payouts(ticker))
  
class Prediction:
  
  def get_future_ETF_price (ticker, years):
    price = data.get_etf_price(ticker)
    growth = data.get_etf_growth(ticker)
    for i in range(years):
      price = price * (1 + growth)
    return float(format(price, ".2f"))
  
  def get_future_dividend_yield (ticker, years):
    price = Prediction.get_future_ETF_price(ticker, years)
    rate = data.get_dividend_rate(ticker)
    dividendYield = price * rate
    return float(format(dividendYield, ".2f"))
  

